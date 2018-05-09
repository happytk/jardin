# -*- coding: utf-8 -*-
"""
    MoinMoin - RecentChanges Macro

    Parameter "ddiffs" by Ralf Zosel <ralf@zosel.com>, 04.12.2003.

    @copyright: 2000-2004 Juergen Hermann <jh@web.de>
    @license: GNU GPL, see COPYING for details.
"""
import time
# import itertools
# import datetime
# import logging

from MoinMoin import util, wikiutil
from MoinMoin.Page import Page, get_middleware_type
from MoinMoin.storage import MoinWikiMiddleware, GitMiddleware
from MoinMoin.logfile import editlog
from MoinMoin import render_template

_DAYS_SELECTION = [1, 2, 3, 7, 14, 30, 60, 90]
_MAX_DAYS = 7
_MAX_PAGENAME_LENGTH = 15  # 35
_MAX_COMMENT_LENGTH = 20

#############################################################################
# RecentChanges Macro
#############################################################################

Dependencies = ["time"]  # ["user", "pages", "pageparams", "bookmark"]


def format_comment(request, line):
    comment = line.comment
    action = line.action
    _ = request.getText
    if action.startswith('ATT'):
        filename = wikiutil.url_unquote(line.extra)
        if action == 'ATTNEW':
            comment = _("Upload of attachment '%(filename)s'.") % {
                'filename': filename}
        elif action == 'ATTDEL':
            comment = _("Attachment '%(filename)s' deleted.") % {
                'filename': filename}
        elif action == 'ATTDRW':
            comment = _("Drawing '%(filename)s' saved.") % {
                'filename': filename}
    elif '/REVERT' in action:
        rev = int(line.extra)
        comment = (_("Revert to revision %(rev)d.") % {'rev': rev}) + " " + comment
    elif '/RENAME' in action:
        comment = (_("Renamed from '%(oldpagename)s'.") % {'oldpagename': line.extra}) + " " + comment

    return wikiutil.make_breakable(comment, _MAX_COMMENT_LENGTH)


def format_page_edits(macro, lines, bookmark_usecs):
    request = macro.request
    _ = request.getText
    d = {}  # dict for passing stuff to theme
    line = lines[0]
    pagename = line.pagename
    rev = int(line.rev)
    tnow = time.time()
    is_new = lines[-1].action == 'SAVENEW'
    is_renamed = lines[-1].action == 'SAVE/RENAME'
    # check whether this page is newer than the user's bookmark
    hilite = line.ed_time_usecs > (bookmark_usecs or line.ed_time_usecs)
    page = Page(request, pagename)

    html_link = ''
    if not page.exists():
        img = request.theme.make_icon('deleted')
        revbefore = rev - 1
        if revbefore and page.exists(rev=revbefore, domain='standard'):
            # indicate page was deleted and show diff to last existing revision of it
            html_link = page.link_to_raw(request, img, querystr={'action': 'diff'}, rel='nofollow')
        else:
            # just indicate page was deleted
            html_link = img
    elif page.isConflict():
        img = request.theme.make_icon('conflict')
        html_link = page.link_to_raw(request, img, querystr={'action': 'edit'}, rel='nofollow')
    elif hilite:
        # show special icons if change was after the user's bookmark
        if is_new:
            img = 'new'
        elif is_renamed:
            img = 'renamed'
        else:
            img = 'updated'
        img = request.theme.make_icon(img)
        html_link = page.link_to_raw(request, img, querystr={'action': 'diff', 'date': '%d' % bookmark_usecs}, rel='nofollow')
    else:
        # show "DIFF" icon else
        img = request.theme.make_icon('diffrc')
        html_link = page.link_to_raw(request, img, querystr={'action': 'diff'}, rel='nofollow')

    # print name of page, with a link to it
    force_split = len(page.page_name) > _MAX_PAGENAME_LENGTH

    d['icon_html'] = html_link
    d['pagelink_html'] = page.link_to(request, text=page.split_title(force=force_split))
    if hasattr(line, 'entry'):
        d['pagelink_html'] += render_template(
            '_dayone_footer.html',
            entry=line.entry, request=request)

    # print time of change
    d['time_html'] = None
    if request.cfg.changed_time_fmt:
        tdiff = long(tnow - wikiutil.version2timestamp(long(line.ed_time_usecs))) / 60 # has to be long for py 2.2.x
        if tdiff < 100:
            d['time_html'] = _("%(mins)dm ago") % {
                'mins': tdiff}
        else:
            d['time_html'] = time.strftime(request.cfg.changed_time_fmt, line.time_tuple)

    # print editor name or IP
    d['editors'] = None
    if request.cfg.show_names:
        if len(lines) > 1:
            counters = {}
            for idx in range(len(lines)):
                name = lines[idx].getEditor(request)
                if name not in counters:
                    counters[name] = []
                counters[name].append(idx+1)
            poslist = [(v, k) for k, v in counters.items()]
            poslist.sort()
            d['editors'] = []
            for positions, name in poslist:
                d['editors'].append("%s&nbsp;[%s]" % (
                    name, util.rangelist(positions)))
        else:
            d['editors'] = [line.getEditor(request)]

    comments = []
    for idx in range(len(lines)):
        comment = format_comment(request, lines[idx])
        if comment:
            comments.append((idx+1, wikiutil.escape(comment)))

    d['changecount'] = len(lines)
    d['comments'] = comments

    img = request.theme.make_icon('info')
    d['info_html'] = page.link_to_raw(request, img, querystr={'action': 'info'}, rel='nofollow')

    return request.theme.recentchanges_entry(d)


def cmp_lines(first, second):
    return cmp(first[0], second[0])


def print_abandoned(macro):
    request = macro.request
    _ = request.getText
    output = []
    d = {}
    page = macro.formatter.page
    pagename = page.page_name
    d['page'] = page
    d['q_page_name'] = wikiutil.quoteWikinameURL(pagename)
    msg = None

    pages = request.rootpage.getPageList()
    last_edits = []
    for name in pages:
        log = Page(request, name).editlog_entry()
        if log:
            last_edits.append(log)
        #   we don't want all Systempages at the beginning of the abandoned list
        #    line = editlog.EditLogLine({})
        #    line.pagename = page
        #    line.ed_time = 0
        #    line.comment = 'not edited'
        #    line.action = ''
        #    line.userid = ''
        #    line.hostname = ''
        #    line.addr = ''
        #    last_edits.append(line)
    del pages
    last_edits.sort()

    # set max size in days
    max_days = min(int(request.values.get('max_days', 0)), _DAYS_SELECTION[-1])
    # default to _MAX_DAYS for users without bookmark
    if not max_days:
        max_days = _MAX_DAYS
    d['rc_max_days'] = max_days

    # give known user the option to extend the normal display
    if request.user.valid:
        d['rc_days'] = _DAYS_SELECTION
    else:
        d['rc_days'] = None

    d['rc_update_bookmark'] = None
    output.append(request.theme.recentchanges_header(d))

    length = len(last_edits)

    index = 0
    last_index = 0
    day_count = 0

    if length > 0:
        line = last_edits[index]
        line.time_tuple = request.user.getTime(wikiutil.version2timestamp(line.ed_time_usecs))
        this_day = line.time_tuple[0:3]
        day = this_day

    while 1:

        index += 1

        if index > length:
            break

        if index < length:
            line = last_edits[index]
            line.time_tuple = request.user.getTime(wikiutil.version2timestamp(line.ed_time_usecs))
            day = line.time_tuple[0:3]

        if (day != this_day) or (index == length):
            d['bookmark_link_html'] = None
            d['date'] = request.user.getFormattedDate(wikiutil.version2timestamp(last_edits[last_index].ed_time_usecs))
            output.append(request.theme.recentchanges_daybreak(d))
            this_day = day

            for page in last_edits[last_index:index]:
                output.append(format_page_edits(macro, [page], None))
            last_index = index
            day_count += 1
            if (day_count >= max_days):
                break

    d['rc_msg'] = msg
    output.append(request.theme.recentchanges_footer(d))
    return ''.join(output)


def logchain(request, log1):
    logs = [
        # (log1, '__wiki__'),  # default wiki recent-logs
    ]
    for name, storage in request.storage.iteritems():
        if isinstance(storage, MoinWikiMiddleware):
            data = log1
        else:
            data = storage.history(request)
        logs.append(
            (data, name)
        )

    # build a bucket for each log-generator
    next_data = []
    for a in range(len(logs)):
        next_data.append(None)

    while True:
        # odt1 = time.time()
        for idx, packed in enumerate(logs):
            s, storage_name = packed
            try:
                if next_data[idx]:
                    pass
                else:
                    # odt = datetime.now()
                    next_data[idx] = next(s)  # if next_data is None, get the next data using 'next(s)'
                    # print(storage_name, datetime.now()-odt)
                    while True:
                        mt = get_middleware_type(request, next_data[idx].pagename)
                        # mt = Page(request, next_data[idx].pagename).middleware_type()
                        if mt == storage_name:
                            break
                        else:
                            next_data[idx] = next(s)
            except StopIteration:
                next_data[idx] = None
        # odt2 = time.time()
        if not max(next_data):  # all is None
            break

        # pick the latest log among storages
        times = []
        for s in next_data:
            if s is None:
                times.append(0)
            else:
                times.append(request.user.getTime(wikiutil.version2timestamp(s.ed_time_usecs))[:5])
        # odt3 = time.time()

        mtime = max(times)
        idx = times.index(mtime)
        ydata = next_data[idx]
        next_data[idx] = None  # invalidate

        # print(odt2-odt1, odt3-odt2, time.time()-odt3)
        yield ydata


def logchain2(request, log1, log2):
    n1_next = None
    n2_next = None
    count = 0
    while True:
        count += 1
        try:
            n1 = n1_next or next(log1)
        except StopIteration:
            n1 = None
        try:
            n2 = n2_next or next(log2)
        except StopIteration:
            n2 = None

        n1_next = n1
        n2_next = n2
        # print count, n1_next, n1.pagename, n2_next, n2.pagename

        if n1 is None and n2 is None:
            break
        elif n1 is not None and n2 is not None:
            t1 = request.user.getTime(wikiutil.version2timestamp(n1.ed_time_usecs))[:5]
            t2 = request.user.getTime(wikiutil.version2timestamp(n2.ed_time_usecs))[:5]
            if t1 > t2:
                n1_next = None
                yield n1
            elif t1 == t2: #same item, discard one.
                n1_next = None
                n2_next = None
                yield n1
            else:
                n2_next = None
                yield n2
        elif n1 is None:
            n2_next = None
            yield n2
        else:
            n1_next = None
            yield n1


def macro_RecentChanges(macro, abandoned=False):
    # handle abandoned keyword

    if abandoned:
        return print_abandoned(macro)

    request = macro.request
    _ = request.getText
    output = []
    user = request.user
    page = macro.formatter.page
    pagename = page.page_name

    d = {}
    d['page'] = page
    d['q_page_name'] = wikiutil.quoteWikinameURL(pagename)

    log = editlog.EditLog(request)

    tnow = time.time()
    msg = ""

    # get bookmark from valid user
    bookmark_usecs = request.user.getBookmark() or 0

    # add bookmark link if valid user
    d['rc_curr_bookmark'] = None
    d['rc_update_bookmark'] = None
    if request.user.valid:
        d['rc_curr_bookmark'] = _('(no bookmark set)')
        if bookmark_usecs:
            currentBookmark = wikiutil.version2timestamp(bookmark_usecs)
            currentBookmark = user.getFormattedDateTime(currentBookmark)
            currentBookmark = _('(currently set to %s)') % currentBookmark
            deleteBookmark = page.link_to(request, _("Delete bookmark"), querystr={'action': 'bookmark', 'time': 'del'}, rel='nofollow')
            d['rc_curr_bookmark'] = currentBookmark + ' ' + deleteBookmark

        version = wikiutil.timestamp2version(tnow)
        d['rc_update_bookmark'] = page.link_to(request, _("Set bookmark"), querystr={'action': 'bookmark', 'time': '%d' % version}, rel='nofollow')

    # set max size in days
    max_days = min(int(request.values.get('max_days', 0)), _DAYS_SELECTION[-1])
    ignore_line_limit = int(request.values.get('ignore_line_limit', 0))
    # default to _MAX_DAYS for useres without bookmark
    if not max_days and not bookmark_usecs:
        max_days = _MAX_DAYS
    d['rc_max_days'] = max_days

    # give known user the option to extend the normal display
    if request.user.valid:
        d['rc_days'] = _DAYS_SELECTION
    else:
        d['rc_days'] = []

    output.append(request.theme.recentchanges_header(d))

    pages = {}
    ignore_pages = {}

    today = request.user.getTime(tnow)[0:3]
    this_day = today
    day_count = 0
    line_count = 0

    # iter_commit of git is heavy. so set the limit.
    LIMIT = 0
    for _dummy, storage in request.storage.iteritems():
        if isinstance(storage, GitMiddleware):
            LIMIT = 30
            break

    for line in logchain(request, log.reverse()):

        if not request.user.may.read(line.pagename):
            continue

        line.time_tuple = request.user.getTime(wikiutil.version2timestamp(line.ed_time_usecs))
        day = line.time_tuple[0:3]
        hilite = line.ed_time_usecs > (bookmark_usecs or line.ed_time_usecs)

        if ((this_day != day or (not hilite and not max_days))) and len(pages) > 0:
            # new day or bookmark reached: print out stuff
            this_day = day
            for p in pages:
                ignore_pages[p] = None
            pages = pages.values()
            pages.sort(cmp_lines)
            pages.reverse()

            if request.user.valid:
                bmtime = pages[0][0].ed_time_usecs
                d['bookmark_link_html'] = page.link_to(request, _("Set bookmark"), querystr={'action': 'bookmark', 'time': '%d' % bmtime}, rel='nofollow')
            else:
                d['bookmark_link_html'] = None
            d['date'] = request.user.getFormattedDate(wikiutil.version2timestamp(pages[0][0].ed_time_usecs))
            output.append(request.theme.recentchanges_daybreak(d))

            # line limit per day
            line_count = 0

            for p in pages:
                output.append(format_page_edits(macro, p, bookmark_usecs))
            pages = {}
            day_count += 1
            if max_days and (day_count >= max_days):
                break

        elif this_day != day:
            # new day but no changes
            this_day = day

        if line.pagename in ignore_pages:
            continue

        # end listing by default if user has a bookmark and we reached it
        if not max_days and not hilite:
            msg = _('[Bookmark reached]')
            break

        if line.pagename in pages:
            pages[line.pagename].append(line)
        else:
            pages[line.pagename] = [line]

        # line limit per day
        if LIMIT and line_count >= LIMIT and not ignore_line_limit and max_days < 8:
            msg = _(u'<div class="alert alert-danger"><i class="fa fa-exclamation-triangle"></i> Exceed log-line-limit(%(limit)d) for the performance. (필요할 경우 <a href="?ignore_line_limit=1">이 링크를 눌러 시도</a>. 그러나 오래걸릴 수도, 실패할 수 있습니다.)</div>') % {
                'limit': LIMIT,
            }
            # logging.warn('LOG[%s] OVER %d LIMIT HAS BEEN STRIPPED' % (str(this_day), LIMIT))
            break
        else:
            line_count += 1

    else:
        if len(pages) > 0:

            # end of loop reached: print out stuff
            # XXX duplicated code from above
            # but above does not trigger if we have the first day in wiki history
            for p in pages:
                ignore_pages[p] = None
            pages = pages.values()
            pages.sort(cmp_lines)
            pages.reverse()

            if request.user.valid:
                bmtime = pages[0][0].ed_time_usecs
                d['bookmark_link_html'] = page.link_to(request, _("Set bookmark"), querystr={'action': 'bookmark', 'time': '%d' % bmtime}, rel='nofollow')
            else:
                d['bookmark_link_html'] = None
            d['date'] = request.user.getFormattedDate(wikiutil.version2timestamp(pages[0][0].ed_time_usecs))
            output.append(request.theme.recentchanges_daybreak(d))

            for p in pages:
                output.append(format_page_edits(macro, p, bookmark_usecs))

    d['rc_msg'] = msg
    output.append(request.theme.recentchanges_footer(d))

    return ''.join(output)
