# -*- coding: utf-8 -*-
"""
MoinMoin - do global changes to all pages in a wiki.

@copyright: 2004-2006 MoinMoin:ThomasWaldmann
@license: GNU GPL, see COPYING for details.
"""

import os
import sys
import shutil

from MoinMoin.Page import Page
from MoinMoin import wikiutil
from MoinMoin.action import AttachFile
from MoinMoin.script import MoinScript

class PluginScript(MoinScript):

    def __init__(self, argv, def_values):
        MoinScript.__init__(self, argv, def_values)

        self.parser.add_option("-t", "--target-repo", dest="target_repo", help="")

    def mainloop(self):

        self.init_request()

        request = self.request
        target = self.options.target_repo

        if target not in request.cfg.middlewares:
            print '{0} repo does not exists.'.format(target)
            sys.exit(0)

        target = request.storage[target]

        pagelist = list(request.rootpage.getPageList(user=''))
        for pagename in pagelist:
            pagename_fs = wikiutil.quoteWikinameFS(pagename)
            # print 'processing..', pagename, pagename_fs

            source_page = Page(request, pagename)
            target_page = target.get_adaptor(request, pagename_fs)

            body = source_page.get_raw_body()
            target_page.is_write_file(body)

            for fp in AttachFile._get_files(request, pagename):
                # print 'processing attachments..', fp
                fp = os.path.join(AttachFile.getAttachDir(request, pagename), fp)
                try:
                    if os.path.isfile(fp):
                        target_page.import_attachment(fp, copy=True)
                    else:
                        raise Exception()
                except:
                    print '[error to import]', fp
