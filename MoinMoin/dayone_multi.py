#-*-encoding:utf-8-*-
import sys
import os
import stat
import uuid as pyuuid
import re
import plistlib
import datetime
import glob
import time
import calendar
from MoinMoin.storage import PageAdaptor
from MoinMoin.logfile import editlog
from MoinMoin.Page import Page
from MoinMoin import wikiutil
from MoinMoin import log
from MoinMoin import render_template
from werkzeug import escape

logging = log.getLogger(__name__)


class DayoneMiddleware:

    def __init__(self, path, prefix='', restrict_user=None, format='text_markdown'):
        self.path = path
        self.prefix = prefix
        self.user = restrict_user
        self.basepath = os.path.join(os.path.abspath(path), 'entries')
        self.format = format
        # print 'hello'

    def get_adaptor(self, request, pagename_fs):
        # , self.basepath, self.prefix, self.user)
        return DayonePageAdaptor(request, pagename_fs[len(self.prefix):], self)

    def history(self, request):
        # allowed-user could get the history.
        if True: # not self.user or (request.user.valid and request.user.name == self.user):
            # files = sorted(files, lambda x,y:os.path.getmtime(x) < os.path.getmtime(y), reverse=True)

            if hasattr(request.cfg, 'redis'):
                files = request.cfg.redis.zrange('dayone_ordered_entry_' + self.prefix, 0, -1, \
                                desc=True, withscores=True)
            else:
                # if redis is not possible
                # ordering by created_time should be big burden.
                files = map(lambda x: (x, os.path.getmtime(x)), self._list_files(request))
                files = sorted(
                    files, key=lambda x: x[1], reverse=True)

            _usercache = {}
            for filename, ed_time_usecs in files:
                result = editlog.EditLogLine(_usercache)
                result.rev = 0
                result.action = 'SAVE'
                result.pagename = wikiutil.unquoteWikiname(
                    self.prefix + os.path.splitext(os.path.basename(filename))[0])
                result.addr = ''
                result.hostname = ''
                result.userid = self.user
                # if self.user:
                #     result.userid = request.user.id # restrict_user is self
                # else:
                #     result.userid = ''
                result.extra = None
                result.comment = ''
                result.ed_time_usecs = wikiutil.timestamp2version(ed_time_usecs)

                # IT IS POSSIBLE TO CAUSE BAD PERFORMANCE
                result.entry = Entry(self, filename)

                yield result

    def _list_files(self, request):
        lst = glob.glob(os.path.join(self.basepath, "*.doentry"))
        # logging.error(self.prefix)
        # logging.error(lst[:10])
        conflict_filter = lambda x: 'conflicted copy' not in x
        return filter(conflict_filter, lst)

    def list_pages(self, request):
        # if not self.user or (request.user.valid and request.user.name ==
        # self.user):
        fnfilter = lambda x: wikiutil.unquoteWikiname(
            self.prefix + os.path.splitext(os.path.basename(x))[0])
        return map(fnfilter, self._list_files(request))

    def filter_by_tag(self, request, tagname):
        if hasattr(request.cfg, 'redis') and request.cfg.redis:
            key = 'dayone_tag_' + self.prefix + tagname
            # logging.critical('x'*100)
            # logging.critical(key)
            # logging.critical('x'*100)
            return request.cfg.redis.smembers(key)
        else:
            # logging.critical('y'*100)
            # logging.critical(tagname)
            # logging.critical('y'*100)

            # print '-'*1000, tagname
            # fnfilter = lambda x: wikiutil.unquoteWikiname(self.prefix + os.path.splitext(os.path.basename(x))[0])
            entries = map(lambda x: Entry(self, x), self._list_files(request))
            # for entry in entries:
            #     print entry.tags, entry.starred
            entries = filter(lambda x: tagname in x.tags,
                             entries)  # and not x.starred
            # for entry in entries:
            #     print entry.tags, entry.starred, entry.filename, self.prefix
            # fnfilter = lambda x: wikiutil.unquoteWikiname(self.prefix + os.path.splitext(os.path.basename(x.filename))[0])
            return map(lambda x: x.pagename, entries)

    def refresh_redis(self, redisobj, empty=False):
        # empty
        if empty:
            keys = [r for r in redisobj.keys() if r.startswith(
                'dayone_tag_' + self.prefix)]
            for key in keys:
                redisobj.delete(key)

        # building
        entries = map(lambda x: Entry(self, x), self._list_files(None))
        for entry in entries:

            # tagging
            for tag in entry.tags:
                redisobj.sadd('dayone_tag_' + self.prefix +
                              tag, entry.pagename)
            else:
                # untagged entry
                redisobj.sadd('dayone_tag_' + self.prefix, entry.pagename)

            # ordering (for recentchanges)
            #for entry in y.tags:
            redisobj.zadd('dayone_ordered_entry_' + self.prefix, entry.filename, entry.timestamp)

        return


class DayonePageAdaptor(PageAdaptor):

    def __init__(self, request, pagename_fs, middleware):
        PageAdaptor.__init__(self, request, pagename_fs)
        self.pagename_fs = self.request.cfg.pagename_router(pagename_fs)
        self.path = middleware.basepath
        self.filepath = middleware.basepath + os.sep + pagename_fs + '.doentry'
        self.e = None
        self.prefix = middleware.prefix
        self.user = middleware.user

    def _get_entry(self):
        if self.e:
            return self.e

        # try to open file
        try:
            self.e = Entry(self, self.filepath)
        except IOError, er:
            import errno
            if er.errno == errno.ENOENT:
                # just doesn't exist, return empty text (note that we
                # never store empty pages, so this is detectable and also
                # safe when passed to a function expecting a string)
                return None
            else:
                raise

        return self.e

    def get_body(self):

        e = self._get_entry()

        try:
            # if len(e.tags):
            #     text = e.text
            # else:
            text = e.text
            # if re.match('[A-Z0-9]{32}', self.pagename_fs):
            #     text = '#acl All:\n#format text_markdown\n' + text

        except:
            text = ''
        finally:
            pass

        return text

    def text(self):
        # this text will be shown as pagename at wikipages
        return '[%s]%s..' % (self.prefix, escape(self.get_body()[:20]))

    def exists(self, rev=0, domain=None, includeDeleted=False):
        return os.path.isfile(self.filepath)

    def is_write_file(self, newtext):
        # save to page file
        e = self._get_entry()
        # Write the file using text/* mime type
        # newtext = newtext.replace(r'#acl All:', '').replace(r'#format
        # text_markdown', '').strip()
        e.text = newtext
        # if not re.match('[A-Z0-9]{32}', self.pagename_fs):
        #     # e.date = datetime.datetime.today()
        #     e.starred = True

        #     pagename = wikiutil.unquoteWikiname(self.pagename_fs)
        #     if not e.has_tag(pagename):
        #         e.addtag(pagename)

        try:
            if not e.date:
                e.date = datetime.datetime.utcnow()
        except KeyError:
            e.date = datetime.datetime.utcnow()
        # try:
        #     if not e.uuid:
        #         e.uuid = str(pyuuid.uuid1()).upper().replace('-', '')
        # except KeyError:
        #     e.uuid = str(pyuuid.uuid1()).upper().replace('-', '')
        e.uuid = self.pagename_fs
        e.save()

        return True

    @property
    def created_at(self):
        return self._get_entry().timestamp

    def last_modified(self):
        return os.path.getmtime(self.filepath)

    def isWritable(self):
        return os.access(self.filepath, os.W_OK) or not self.exists()

    def delete(self):
        os.remove(self.filepath)

    def header(self):
        return render_template('_dayone_header.html', entry=self._get_entry(), prefix=self.prefix, request=self.request)

    def lastEditInfo(self, request=None):
        time = wikiutil.version2timestamp(self.last_modified())
        if request:
            time = request.user.getFormattedDateTime(
                time)  # Use user time format
        else:
            time = datetime.datetime.fromtimestamp(
                time * 1000 * 1000).strftime('%Y-%m-%d %H:%M:%S')  # Use user time format
        return {'editor': self.user, 'time': time}

    def footer(self):
        return render_template('_dayone_footer.html', entry=self._get_entry(), request=self.request)


class Entry(object):

    def __init__(self, journal, filename=None):
        self._entry = {}
        self.journal = journal
        self.filename = filename
        self.pagename = wikiutil.unquoteWikiname(
            self.journal.prefix + os.path.splitext(os.path.basename(filename))[0])
        if filename is not None:
            self.load()

    def load(self, filename=None):
        if filename is None:
            filename = self.filename
        try:
            self._entry = plistlib.readPlist(filename)
        except:  # IOError
            self._entry = {'UUID':''}

    def save(self, filename=None):
        if filename is None:
            filename = self.filename
        self._entry["Time Zone"] = "Asia/Seoul"
        self._entry["Activity"] = "Stationary"
        if 'Creation Date' not in self._entry:
            self._entry['Creation Date'] = datetime.datetime.utcnow()

        plistlib.writePlist(self._entry, filename)

    def remove(self, filename=None):
        if filename is None:
            filename = self.filename
        os.remove(filename)

    @property
    def uuid(self): return self._entry["UUID"]

    @uuid.setter
    def uuid(self, x):
        self._entry["UUID"] = str(x)

    @property
    def text(self): return self._entry["Entry Text"]

    @text.setter
    def text(self, x):
        self._entry["Entry Text"] = unicode(x)

    @property
    def date(self):
        try:
            return self._entry["Creation Date"]
        except KeyError:
            return datetime.datetime.now()


    @date.setter
    def date(self, x):
        if not isinstance(x, datetime.datetime):
            raise ValueError, "date must be a datetime object"
        self._entry["Creation Date"] = x

    @property
    def timestamp(self):
        try:
            d = self._entry["Creation Date"]
            return calendar.timegm(d.timetuple())
        except KeyError:
            return time.time()



    @property
    def starred(self):
        try:
            return self._entry["Starred"]
        except:
            return False

    @starred.setter
    def starred(self, x):
        self._entry["Starred"] = bool(x)

    # Tags
    @property
    def tags(self): return self._entry.get("Tags", [])

    @tags.setter
    def tags(self, x):
        self._entry["Tags"] = list(x)

    def wikitags(self, request):
        pages = [Page(request, tag) for tag in self.tags]
        pages = [p for p in pages if p.exists()]
        return pages

    def addtag(self, tag):
        if not self._entry.get("Tags", None):
            self._entry["Tags"] = []
        if tag not in self._entry["Tags"]:
            self._entry["Tags"].append(tag)

    def rmtag(self, tag):
        if tag in self._entry["Tags"]:
            self._entry["Tags"].remove(tag)

    def has_tag(self, tag):
        return tag in self.tags

    def pagename(self):
        return ''.join(self._entry.get("Tags", []))

    def last_modified(self):
        return os.path.getmtime(self.filename)

    # Location not implemented yet
    @property
    def location(self): return self._entry.get("Location", {})

    # Weather not implemented yet
    @property
    def weather(self): return self._entry.get("Weather", {})

    # Return the picture if there is one, not implemented yet
    @property
    def picture(self):
        fn = os.path.join(os.path.split(self.journal.path)[
                          0], "photos", "%s.jpg" % (str(self.uuid).upper(),))
        # print fn
        if os.path.isfile(fn):
            # from PIL import Image
            # im = Image.open(fn)
            # if im.size[0] > 800:
            #     img_width = 800
            # else:
            #     img_width = im.size[0]
            return "%s.jpg" % str(self.uuid).upper()
        return None
