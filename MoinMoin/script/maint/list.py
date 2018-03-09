# -*- coding: utf-8 -*-
"""
MoinMoin - do global changes to all pages in a wiki.

@copyright: 2004-2006 MoinMoin:ThomasWaldmann
@license: GNU GPL, see COPYING for details.
"""

debug = False

from MoinMoin import PageEditor
from MoinMoin.script import MoinScript

class PluginScript(MoinScript):
    """\
Purpose:
========
This tool allows you to list up all the pages in a wiki.

Detailed Instructions:
======================
General syntax: moin [options] maint list

[options] usually should be:
    --config-dir=/path/to/my/cfg/ --wiki-url=http://wiki.example.org/

"""

    def __init__(self, argv, def_values):
        MoinScript.__init__(self, argv, def_values)

    def mainloop(self):
        self.init_request()
        request = self.request
        request.cfg.all_pages_exclude_dayone = True

        # Get all existing pages in the wiki
        pagelist = request.rootpage.getPageList(user='', include_underlay=False)

        for pagename in pagelist:
            print pagename.encode('utf8')
