# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - RecentChangeSummury Macro

    This very complicated macro produces a line break.

    @copyright: 2006 HappyTk (rainyblue-gmail)
    @license: GNU GPL, see COPYING for details.
"""

import time
from datetime import datetime
from MoinMoin.Page import Page
from MoinMoin import wikiutil
from MoinMoin.logfile import editlog
from MoinMoin.parser.text_moin_wiki import Parser as WikiParser
from MoinMoin.macro.RecentChanges import logchain


def getPageListFromLog(macro, req_year, req_week_number, comments_only):
    request = macro.request
    pages = {}

    log = editlog.EditLog(request)
    for line in logchain(request, log.reverse()):
        if not request.user.may.read(line.pagename):
            continue

        line.time_tuple = request.user.getTime(wikiutil.version2timestamp(line.ed_time_usecs))
        year, wn, wd = datetime.isocalendar(datetime.fromtimestamp(time.mktime(line.time_tuple)))
        yw = '%04d%02d' % (year, wn)

        # import logging
        # logging.critical(str([year, wn, req_year, req_week_number]))

        if req_year > 0 and req_week_number > 0:
            if req_week_number == wn and req_year == year:
                pass
            elif (req_week_number > wn and req_year == year) or req_year > year:
                break
            else:
                continue

        if not pages.has_key(yw):
            pages[yw] = {}

        if pages[yw].has_key(line.pagename):
            pages[yw][line.pagename].append(dict(userid=line.userid, comment=line.comment))
        else:
            pages[yw][line.pagename] = [dict(userid=line.userid, comment=line.comment)]

    ret = []
    for yw in sorted(pages.keys()):
        if len(pages[yw].keys()) > 0:
            ret.append("WEEK%s, %s" % (yw[-2:], yw[:4]))
            for page in reversed(sorted(pages[yw].keys(), key=lambda x: len(pages[yw][x]))):
                edit_cnt = len(pages[yw][page])
                comments = map(lambda x: x['comment'], filter(lambda x: len(x['comment'])>0, pages[yw][page]))
                userids = set(map(lambda x:x['userid'], pages[yw][page]))

                p = Page(request, page)

                if len(comments) > 0 or not comments_only:
                    if p.exists():
                        ret.append(' - [[%s]] (edited %s) <<HTML(<i class="fa fa-user"></i>)>> %s' % (page, str(edit_cnt), ','.join(userids)))
                    else:
                        ret.append(' - `%s` (edited %s) <<HTML(<i class="fa fa-user"></i>)>> %s' % (page, str(edit_cnt), ','.join(userids)))
                    for comment in comments:
                        ret.append('  - ' + comment)

#     macro_str = "<<%s>>" % (macro.name)
#     content_str = '\n'.join(ret)
#     form = u'''<form method='post'>
#     <input type='hidden' name='action' value='ReplaceTagAction'>
#     <input type='hidden' name='rsv' value='0'>
#     <input type='hidden' name='regexp' value='0'>
#     <textarea name='tag' style='display:none'>%s</textarea>
#     <textarea name='txt' style='display:none'>%s</textarea>
#     <input type='submit' value='   HARDCOPY TO THIS PAGE   '>
# </form>
# ''' % (macro_str, content_str)

#     return wikiutil.renderText(request, WikiParser, content_str) + form
    return wikiutil.renderText(request, WikiParser, '\n'.join(ret))


def macro_RecentChangeSummury(macro, year=0, week_number=0, comments_only=False):

    if year == 0 and week_number == 0:
        year, week_number, wd = datetime.isocalendar(datetime.today())

    return getPageListFromLog(macro, year, week_number, comments_only)
