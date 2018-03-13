import glob
import re
import os
import datetime
import codecs

from git import Actor, GitCommandError

# try:
#     import dayone
# except ImportError:
#     class dayone:
#         def __init__(self, *args, **kwargs):
#             pass

try:
    from hatta.storage import WikiStorage as HattaWikiStorage

    class WikiStorage(HattaWikiStorage):

        def _title_to_file(self, title):
            filename = title.strip() + self.extension
            return os.path.join(self.repo_prefix, filename)

        def _file_to_title(self, filepath):
            _ = self._
            if not filepath.startswith(self.repo_prefix):
                raise Exception(
                    u"Can't read or write outside of the pages repository")
            name = filepath[len(self.repo_prefix):].strip('/')
            # Un-escape special windows filenames and dot files
            # if name.startswith('_') and len(name) > 1:
            #     name = name[1:]
            if self.extension and name.endswith(self.extension):
                name = name[:-len(self.extension)]
            return name
except ImportError:
    class WikiStorage:

        def __init__(self, *args, **kwargs):
            raise Exception(
                'hatta-package import error -- Need the Hatta package to use the mercurial repository.')


from git import Repo
from dulwich import porcelain

from MoinMoin.logfile import editlog
from MoinMoin import caching
from MoinMoin import wikiutil
from MoinMoin import config
from MoinMoin.Page import WikiPage, WikiRootPage, Page
from MoinMoin import log
from MoinMoin.action import AttachFile
from pprint import pformat
from time import mktime

logging = log.getLogger(__name__)


class PageAdaptor:

    def __init__(self, request, pagename_fs):
        self.request = request
        self.pagename_fs = pagename_fs
        self.pagename = wikiutil.unquoteWikiname(pagename_fs)

    def header(self): return ''
    def footer(self): return ''
    def meta(self, request): return ''

    def text(self): return wikiutil.unquoteWikiname(self.pagename_fs)

    def lastEditInfo(self, request=None): return None

    def getAttachDir(self, check_create=0):
        # return WikiPage(.getPagePath("attachments", check_create=create)
        raise Exception('not_implemented')

    def rename(self, new_pagename_fs):
        pass


class Middleware(object):

    def import_attachment(self, request, pagename, filepath):
        pass

    def remove_attachment(self, request, pagename, filename):
        pass


class MoinWikiMiddleware(Middleware):

    def __init__(self, format=None):
        self.format = format

    def __repr__(self):
        return 'MoinWikiMiddleware'

    def get_adaptor(self, request, pagename_fs):
        return MoinWikiPageAdaptor(request, pagename_fs)

    def history(self, request):
        for i in range(0):
            yield i

    def list_pages(self, request):
        return WikiRootPage(request)._listPages()


class MoinWikiPageAdaptor(PageAdaptor):

    def __init__(self, request, pagename_fs):
        PageAdaptor.__init__(self, request, pagename_fs)
        pagename = wikiutil.unquoteWikiname(pagename_fs)

        # if request.page and pagename == request.page.page_name:
        #     page = request.page # reusing existing page obj is faster
        # else:
        page = WikiPage(request, pagename)

        self.page = page
        self.request = request
        self.pagename = pagename

    def get_body(self):
        return self.page.get_raw_body()

    def exists(self, rev=0, domain=None, includeDeleted=False):
        return self.page.exists(rev, domain, includeDeleted)

    def is_write_file(self, newtext):
        return True

    def last_modified(self):
        return os.path.getmtime(self.page._text_filename())

    def isWritable(self):
        return self.page.isWritable()

    def delete(self):
        pass

    def getAttachDir(self, check_create=0):
        # from MoinMoin.action.AttachFile import getAttachDir
        # return getAttachDir(self.request, self.pagename, create=check_create)

        return self.page.getPagePath("attachments", check_create=check_create)


# def timeit(iterobj):
#     ot1 = datetime.datetime.now()
#     for it in iterobj:
#         ot2 = datetime.datetime.now()
#         yield it
#         print(ot2 - ot1, it)
#         ot1 = ot2


class GitMiddleware(Middleware):

    def __init__(self, path, format=None, subdir=None):
        if subdir:
            self.path = os.path.join(path, subdir)
        else:
            self.path = path
        self.repo = Repo(path)
        self.format = format
        logging.debug('set format -> %s' % format)

    def __repr__(self):
        return 'GitMiddleware[%s]' % self.path

    def history(self, request):
        _usercache = {}
        # odt1 = None
        for commit in self.repo.iter_commits('master'):
            # odt2 = datetime.datetime.now()
            # title, rev, date, author, comment
            date = datetime.datetime.utcfromtimestamp(mktime(commit.committed_datetime.utctimetuple()))
            author = commit.committer.email
            comment = commit.summary
            rev = commit.hexsha

            if len(commit.stats.files) > 5:
                # skip bulk
                continue
            else:
                for entry in commit.stats.files:
                    result = editlog.EditLogLine(_usercache)
                    if entry.endswith('.md'):
                        # result.pagename = wikiutil.unquoteWikiname(entry[:-3])
                        result.pagename = entry[:-3]
                        result.comment = '' if comment == 'comment' or comment.startswith(
                            'MoinEdited:') else comment
                    else:
                        # case of the attachments
                        # if os.sep in entry:
                        #     path, filename = os.path.split(entry)
                        #     result.comment = '%s %s' % (filename, str(commit.stats.files[entry]))
                        #     result.pagename = wikiutil.unquoteWikiname(path)
                        # else:
                        #     continue
                        continue

                    result.ed_time_usecs = wikiutil.timestamp2version(
                        (date - datetime.datetime(1970, 1, 1)).total_seconds())
                    result.rev = 0
                    result.action = 'SAVE'
                    result.addr = ''
                    result.hostname = ''
                    result.userid = author
                    result.extra = None
                    yield result

    def list_pages(self, request):
        # pages = [wikiutil.unquoteWikiname(
        #     page[:-3]) for page in os.listdir(self.path) if page.endswith('.md')]
        # return pages
        import fnmatch
        matches = []
        for root, dirnames, filenames in os.walk(self.path):
            for filename in fnmatch.filter(filenames, '*.md'):
                matches.append(os.path.join(root, filename))
        result = [
            page[len(self.path)+1:-3]
            # for page in os.listdir(self.path)
            for page in matches
            # if page.endswith('md')
        ]
        result = [
            pagename
            for pagename in result
            if not pagename.startswith('_attachments')
        ]
        return result

    def import_attachment(self, request, pagename, filepath):
        # pagename_fs = wikiutil.quoteWikinameFS(pagename)
        self.get_adaptor(request, pagename).import_attachment(filepath)

    def remove_attachment(self, request, pagename, filename):
        # pagename_fs = wikiutil.quoteWikinameFS(pagename)
        # self.get_adaptor(request, pagename_fs).remove_attachment(filename)
        self.get_adaptor(request, pagename).remove_attachment(filename)

    def get_adaptor(self, request, pagename_fs):
        return GitPageAdaptor(request, pagename_fs, self.path, self.repo)


class GitPageAdaptor(PageAdaptor):

    def __init__(self, request, pagename_fs, path, repo):
        PageAdaptor.__init__(self, request, pagename_fs)

        self.repo = repo
        self.path = path
        # self.filepath = self.path + os.sep + \
        #     pagename_fs + request.cfg.fs_extension
        self.filepath = self.path + os.sep + \
            self.pagename + request.cfg.fs_extension
        self.request = request
        self.pagename_fs = pagename_fs

    def meta(self, request):
        try:
            return str(self.repo.git.status())
        except UnicodeEncodeError:
            return ''

    def getAttachDir(self, check_create=0):
        attach_path = os.path.join(self.path, '_attachments', self.pagename)
        if check_create and not os.path.isdir(attach_path):
            try:
                os.makedirs(attach_path)
            except OSError as err:
                if not os.path.exists(attach_path):
                    raise
        return attach_path

    def get_body(self):
        try:
            f = codecs.open(self.filepath, 'rb', config.charset)
        except IOError as er:
            import errno
            if er.errno == errno.ENOENT:
                # just doesn't exist, return empty text (note that we
                # never store empty pages, so this is detectable and also
                # safe when passed to a function expecting a string)
                return ""
            else:
                raise

        try:
            text = f.read()
        finally:
            f.close()

        return text

    def exists(self, rev=0, domain=None, includeDeleted=False):
        return os.path.isfile(self.filepath)

    def is_write_file(self, newtext):
        # # save to page file
        # f = codecs.open(self.filepath, 'wb', config.charset)
        # # Write the file using text/* mime type
        # f.write(newtext)
        # f.close()

        # index = self.repo.index
        # index.add([self.filepath])
        # # mtime_usecs = wikiutil.timestamp2version(os.path.getmtime(pagefile))
        # # # set in-memory content
        # # self.set_raw_body(text)
        # from dulwich.repo import Repo, NotGitRepository
        # request = self.request

        with codecs.open(self.filepath, 'wb', 'utf8') as f:
            f.write(newtext)

        index = self.repo.index
        index.add([self.filepath])

        from git import Actor
        author = Actor("An author", "author@example.com")
        committer = Actor("A committer", "committer@example.com")
        # commit by commit message and author and committer
        ret = index.commit("", author=author, committer=committer)

        self.request.theme.add_msg(
            'Commited to change a text[%s] %s' % (ret.hexsha, pformat(ret.stats.total)), "info")

        return True

    def import_attachment(self, filepath, copy=False):

        if copy:
            import shutil
            dst_filepath = os.path.join(self.getAttachDir(1), os.path.basename(filepath))
            shutil.copyfile(filepath, dst_filepath)

            # destination will be added!
            filepath = dst_filepath

        index = self.repo.index
        index.add([filepath])

        from git import Actor
        author = Actor("An author", "author@example.com")
        committer = Actor("A committer", "committer@example.com")
        # commit by commit message and author and committer
        ret = index.commit("my commit message", author=author, committer=committer)

        self.request.theme.add_msg(
            'Commited to import a attachment[%s] %s' % (ret.hexsha, pformat(ret.stats.total)), "info")

    def last_modified(self):
        return os.path.getmtime(self.filepath)

    def isWritable(self):
        return os.access(self.filepath, os.W_OK) or not self.exists()

    def rename(self, new_pagename_fs):
        index = self.repo.index

        from git import Actor
        head, tail = os.path.split(self.filepath)
        index.add([os.path.join(head, new_pagename_fs + '.md')])
        index.remove([self.filepath])
        # delete physical files
        os.remove(self.filepath)

        target, tail = os.path.splitext(self.filepath)
        if os.path.exists(target):
            for fp in AttachFile._get_files(self.request, self.pagename):
                index.remove([os.path.join(target, fp)])
            new_target = os.path.join(head, new_pagename_fs)
            os.rename(target, new_target)
            for fp in AttachFile._get_files(self.request, new_pagename_fs):
                index.add([os.path.join(new_target, fp)])

        author = Actor("An author", "author@example.com")
        committer = Actor("A committer", "committer@example.com")
        # commit by commit message and author and committer
        ret = index.commit("renamed", author=author, committer=committer)
        self.request.theme.add_msg(
            'Commited to rename[%s] %s' % (ret.hexsha, pformat(ret.stats.total)), "info")



    def delete(self):
        from git import Actor, GitCommandError

        index = self.repo.index
        try:
            index.remove([self.filepath])
        except GitCommandError: pass

        for fp in AttachFile._get_files(self.request, self.pagename):
            try:
                index.remove(fp)
            except GitCommandError: pass

        author = Actor("An author", "author@example.com")
        committer = Actor("A committer", "committer@example.com")
        # commit by commit message and author and committer
        ret = index.commit("deleted", author=author, committer=committer)
        self.request.theme.add_msg(
            'Commited to remove[%s] %s' % (ret.hexsha, pformat(ret.stats.total)), "info")

        # delete physical files
        os.remove(self.filepath)
        if os.path.exists(self.getAttachDir(0)):
            import shutil
            shutil.rmtree(self.getAttachDir(0))

    def remove_attachment(self, filename):
        index = self.repo.index
        filepath = os.path.join(self.getAttachDir(0), filename)

        try:
            index.remove([filepath])
        except GitCommandError:
            logging.critical('Target file seems to be not in git-repo: ' + filepath)
            self.request.theme.add_msg(
            'Target file seems to be not in git-repo: ' + filepath, "warning")
            return

        from git import Actor
        author = Actor("An author", "author@example.com")
        committer = Actor("A committer", "committer@example.com")
        # commit by commit message and author and committer
        ret = index.commit("my commit message", author=author, committer=committer)
        self.request.theme.add_msg(
            'Commited to remove a attachment[%s] %s' % (ret.hexsha, pformat(ret.stats.total)), "info")

        if os.path.exists(filepath):
            os.remove(filepath)

        if len(os.listdir(self.getAttachDir(0))) <= 0:
            import shutil
            shutil.rmtree(self.getAttachDir(0))

class MercurialMiddleware(Middleware):

    def __init__(self, path, format=None):
        self.path = path
        self.hgdb = WikiStorage(path, extension='.md')
        self.format = format
        logging.debug('set format -> %s' % format)

    def get_adaptor(self, request, pagename_fs):
        return MercurialPageAdaptor(request, pagename_fs, self.hgdb)

    def history(self, request):
        _usercache = {}
        for title, rev, date, author, comment in self.hgdb.history():
            if comment.startswith('HgHidden:'):
                continue
            result = editlog.EditLogLine(_usercache)
            result.ed_time_usecs = wikiutil.timestamp2version(
                (date - datetime.datetime(1970, 1, 1)).total_seconds())
            result.rev = rev
            result.action = 'SAVE'
            # result.pagename = wikiutil.unquoteWikiname(title)
            result.pagename = title
            result.addr = ''
            result.hostname = ''
            result.userid = author
            result.extra = None
            result.comment = '' if comment == 'comment' or comment.startswith(
                'MoinEdited:') else comment
            yield result

    def list_pages(self, request):
        pages = [wikiutil.unquoteWikiname(page)
                 for page in self.hgdb.all_pages()]
        return pages


class MercurialPageAdaptor(PageAdaptor):

    def __init__(self, request, pagename_fs, hgdb):
        PageAdaptor.__init__(self, request, pagename_fs)
        self.hgdb = hgdb

    def get_body(self):
        pagename_fs = self.request.cfg.pagename_router(self.pagename_fs)
        try:
            hg_text = self.hgdb.page_text(pagename_fs)
        except:
            hg_text = None
        return hg_text

    def exists(self, rev=0, domain=None, includeDeleted=False):
        # if self.request.cfg.is_target(self.pagename_fs):
        #     return True
        if self.pagename_fs in self.hgdb:
            return True
        return False

    def is_write_file(self, newtext):
        pagename_fs = self.request.cfg.pagename_router(self.pagename_fs)
        newtext = newtext.encode('utf8')
        author = self.request.user.valid and self.request.user.id or ''
        comment = 'MoinEdited: ' + wikiutil.unquoteWikiname(pagename_fs)
        self.hgdb.save_data(
            pagename_fs, newtext, author=author, comment=comment, parent_rev=None)
        return True

    def last_modified(self):
        pagename_fs = self.request.cfg.pagename_router(self.pagename_fs)
        return self.hgdb.page_meta(pagename_fs)[1]

    def isWritable(self):
        # return os.access(self._text_filename(), os.W_OK) or not self.exists()
        # return not self.exists()
        return True

    def delete(self):
        self.hgdb.delete_page(self.pagename_fs, '', '')


# class DayoneMiddleware:
#     def __init__(self, path):
#         self.path = path
#         self.dodb = dayone.Journal(path=path)
#     def get_adaptor(self, request, pagename_fs):
#         return DayonePageAdaptor(request, pagename_fs, self.dodb)
#     def history(self, request):
#         for i in range(0):
#             yield i
#     def list_pages(self, request):
#         return []

# class DayonePageAdaptor(PageAdaptor):
#     def __init__(self, request, pagename_fs, dodb):
#         PageAdaptor.__init__(self, request, pagename_fs)

#         #todo- request
#         self.dodb = dodb
#         self.uuid = self.pagename_fs[len('DayOne(2f)'):]

#     def get_body(self):
#         entry = self.dodb.get(self.uuid)
#         return entry.text

#     def exists(self):
#         return True

#     def is_write_file(self, newtext):
#         e = self.dodb.get(self.uuid)
#         e.text = newtext
#         e.save()
#         return False

#     def last_modified(self):
#         # request.last_modified = os.path.getmtime(self._text_filename()) self.hgdb.page_meta(self.page_name_fs)[1]
#         return None

#     def isWritable(self):
#         # return os.access(self._text_filename(), os.W_OK) or not self.exists()
#         #return not self.exists()
#         return True

#     def delete(self):
#         pass


class PlatfileMiddleware(Middleware):

    def __init__(self, path, format=None):
        self.path = path
        self.basepath = os.path.abspath(path)
        self.format = format

    def __repr__(self):
        return 'PlatfileMiddleware[%s]' % self.basepath

    def get_adaptor(self, request, pagename_fs):
        return PlatfilePageAdaptor(request, pagename_fs, self.path)

    def history(self, request):
        files = self._list_files(request)
        files = sorted(files, lambda x, y: os.path.getmtime(
            x) < os.path.getmtime(y), reverse=True)
        _usercache = {}
        for filename in files:
            result = editlog.EditLogLine(_usercache)
            result.ed_time_usecs = wikiutil.timestamp2version(
                os.path.getmtime(filename))
            result.rev = 0
            result.action = 'SAVE'
            result.pagename = wikiutil.quoteWikinameFS(
                os.path.splitext(os.path.basename(filename))[0].decode(request.cfg.fs_encoding))
            result.addr = ''
            result.hostname = ''
            result.userid = ''
            result.extra = None
            result.comment = ''
            yield result

    def _list_files(self, request):
        return glob.glob(os.path.join(self.basepath, '*' + request.cfg.fs_extension))

    def list_pages(self, request):
        fnfilter = lambda x: wikiutil.quoteWikinameFS(
            os.path.splitext(os.path.basename(x))[0].decode(request.cfg.fs_encoding))
        return map(fnfilter, self._list_files(request))


class PlatfilePageAdaptor(PageAdaptor):

    def __init__(self, request, pagename_fs, basepath):
        PageAdaptor.__init__(self, request, pagename_fs)

        pagename_fs = self.request.cfg.pagename_router(pagename_fs)

        self.basepath = os.path.abspath(basepath)
        self.filepath = self.basepath + os.sep + \
            pagename_fs + request.cfg.fs_extension

    def get_body(self):
        # try to open file
        try:
            f = codecs.open(self.filepath, 'rb', config.charset)
        except IOError as er:
            import errno
            if er.errno == errno.ENOENT:
                # just doesn't exist, return empty text (note that we
                # never store empty pages, so this is detectable and also
                # safe when passed to a function expecting a string)
                return ""
            else:
                raise

        try:
            text = f.read()
        finally:
            f.close()

        return text

    def exists(self, rev=0, domain=None, includeDeleted=False):
        return os.path.isfile(self.filepath)

    def is_write_file(self, newtext):
        # save to page file
        f = codecs.open(self.filepath, 'wb', config.charset)
        # Write the file using text/* mime type
        f.write(newtext)
        f.close()

        # mtime_usecs = wikiutil.timestamp2version(os.path.getmtime(pagefile))
        # # set in-memory content
        # self.set_raw_body(text)
        return True

    def last_modified(self):
        return os.path.getmtime(self._text_filename())

    def isWritable(self):
        return os.access(self.filepath, os.W_OK) or not self.exists()

    def delete(self):
        os.remove(self.filepath)


periods_re = re.compile(r'^[.]|(?<=/)[.]')
slashes_re = re.compile(r'^[/]|(?<=/)[/]')


class DirectoryPlatfileMiddleware(Middleware):

    def __init__(self, path, format=None):
        self.path = path
        self.basepath = os.path.abspath(path)
        self.format = format

    def __repr__(self):
        return 'DirectoryPlatfileMiddleware[%s]' % self.basepath

    def get_adaptor(self, request, pagename_fs):
        return DirectoryPlatfilePageAdaptor(request, pagename_fs, self.path)

    def list_pages(self, request):
        # fnfilter = lambda x: wikiutil.quoteWikinameFS(os.path.splitext(os.path.basename(x))[0])
        # fnfilter = lambda x: wikiutil.quoteWikinameFS(os.path.splitext(os.path.basename(x))[0].decode(request.cfg.fs_encoding))
        def _f(fn):
            fn = os.path.basename(fn)
            if fn.endswith(request.cfg.fs_extension):
                fn = fn[:-len(request.cfg.fs_extension)]
            fn = fn.decode(request.cfg.fs_encoding)
            # fn = wikiutil.quoteWikinameFS(fn)
            return fn
        return map(_f, self._list_files())

    def _list_files(self):
        pages = []
        for root, dirs, files in os.walk(self.basepath):
            for name in dirs:
                pages.append(
                    os.path.join(root, name)[len(self.basepath)+1:].replace(os.sep, '/'))
            for name in files:
                pages.append(
                    os.path.join(root, name)[len(self.basepath)+1:].replace(os.sep, '/'))
        return pages

    def history(self, request):
        # files = self._list_files()
        pages = []
        for root, dirs, files in os.walk(self.basepath):
            for name in dirs:
                pages.append(os.path.join(root, name))
            for name in files:
                pages.append(os.path.join(root, name))

        # pages = sorted(pages, lambda x,y: os.path.getmtime(x) < os.path.getmtime(y), reverse=True)
        # logging.warning(str(pages))
        pages = sorted(pages, key=lambda x: os.path.getmtime(x), reverse=True)

        _usercache = {}
        for filename in pages:
            result = editlog.EditLogLine(_usercache)
            result.ed_time_usecs = wikiutil.timestamp2version(
                os.path.getmtime(filename))
            result.rev = 0
            result.action = 'SAVE'
            filename = filename[len(self.basepath)+1:].replace(os.sep, '/')
            if filename.endswith(request.cfg.fs_extension):
                filename = filename[:-len(request.cfg.fs_extension)]
            result.pagename = filename.decode(request.cfg.fs_encoding)
            result.addr = ''
            result.hostname = ''
            result.userid = ''
            result.extra = None
            result.comment = ''
            yield result


class DirectoryPlatfilePageAdaptor(PageAdaptor):

    def __init__(self, request, pagename_fs, basepath):
        PageAdaptor.__init__(self, request, pagename_fs)

        # logging.warning(pagename_fs)
        pagename_fs = self.request.cfg.pagename_router(pagename_fs)

        pagename = wikiutil.unquoteWikiname(pagename_fs)
        # escaped = werkzeug.url_quote(escaped, safe='/ ')
        # escaped = periods_re.sub('%2E', escaped)
        # escaped = slashes_re.sub('%2F', escaped)
        self.pagename = pagename
        self.filename = pagename
        if len(os.path.splitext(pagename)[1]) == 0 or len(os.path.splitext(pagename)[1]) > 4:
            self.filename += request.cfg.fs_extension

        basepath = os.path.abspath(basepath)
        self.filepath = os.path.join(basepath, self.filename)
        self.basepath = os.path.dirname(self.filepath)
        # print self.filepath

    def get_body(self):
        # try to open file
        try:
            f = codecs.open(self.filepath, 'rb', config.charset)
        except IOError as er:
            import errno
            if er.errno == errno.ENOENT:
                # just doesn't exist, return empty text (note that we
                # never store empty pages, so this is detectable and also
                # safe when passed to a function expecting a string)
                return ""
            else:
                raise

        try:
            text = f.read()
        finally:
            f.close()

        return text

    def exists(self, rev=0, domain=None, includeDeleted=False):
        return os.path.isfile(self.filepath)

    def is_write_file(self, newtext):

        if not os.path.isdir(self.basepath):
            os.makedirs(self.basepath)

        # print '*'*10, self.filepath

        # save to page file
        f = codecs.open(self.filepath, 'wb', config.charset)
        # Write the file using text/* mime type
        f.write(newtext)
        f.close()

        # mtime_usecs = wikiutil.timestamp2version(os.path.getmtime(pagefile))
        # # set in-memory content
        # self.set_raw_body(text)
        return True

    def last_modified(self):
        return os.path.getmtime(self.filepath)

    def isWritable(self):
        return os.access(self.filepath, os.W_OK) or not self.exists()

    def delete(self):
        os.remove(self.filepath)

        # remove if emtpy.
        try:
            os.removedirs(self.basepath)
        except:
            pass
