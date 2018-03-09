# -*- coding: utf-8 -*-
"""
MoinMoin - do global changes to all pages in a wiki.

@copyright: 2004-2006 MoinMoin:ThomasWaldmann
@license: GNU GPL, see COPYING for details.
"""

import os
import sys
import shutil

from MoinMoin import Page
# from MoinMoin.storage import , DirectoryPlatfileMiddleware, MercurialMiddleware, PlatfileMiddleware, MoinWikiMiddleware
from MoinMoin.script import MoinScript

class PluginScript(MoinScript):

    def __init__(self, argv, def_values):
        MoinScript.__init__(self, argv, def_values)

        self.parser.add_option("-s", "--source-repo", dest="source_repo", help="")
        self.parser.add_option("-t", "--target-repo", dest="target_repo", help="")

    def mainloop(self):

        self.init_request()

        request = self.request
        source = self.options.source_repo
        target = self.options.target_repo

        if source not in request.cfg.middlewares:
            print '{0} repo does not exists.'.format(source)
            sys.exit(0)

        if target not in request.cfg.middlewares:
            print '{0} repo does not exists.'.format(target)
            sys.exit(0)

        source = request.storage[source]
        target = request.storage[target]

        for pagename_fs in source.list_pages(request):
            print 'processing..', pagename_fs

            source_page = source.get_adaptor(request, pagename_fs)
            target_page = target.get_adaptor(request, pagename_fs)

            body = source_page.get_body()
            target_page.is_write_file(body)

            if os.path.exists(source_page.getAttachDir()):
                print 'processing attachments..', source_page.getAttachDir()
                shutil.copy(source_page.getAttachDir(), target_page.getAttachDir())

        # configuration

        # 'hg1': (MercurialMiddleware,         (os.path.abspath(os.path.dirname(__file__)) + '\moinhg1',)),
        # 'hg2': (MercurialMiddleware,         (os.path.abspath(os.path.dirname(__file__)) + '\moinhg2',)),
        # 'fs1': (DirectoryPlatfileMiddleware, (os.path.abspath(os.path.dirname(__file__)) + '\moindpl',)),
        # 'fs2': (PlatfileMiddleware,          (os.path.abspath(os.path.dirname(__file__)) + '\moinpl',)),
        # 'wiki': (MoinWikiMiddleware,         ()),
        # 'dayone': (DayoneMiddleware,         ('/volume1/dropbox_rainyblue/Apps/Day One/Journal.dayone',)),

        # src, target
        # data_hg_dir = 'd:/__cloud/moinprv'
        # source = MercurialMiddleware(data_hg_dir)

        # data_dpl_dir = 'd:/__cloud/prv_target'
        # target = DirectoryPlatfileMiddleware(data_dpl_dir)

        # #read source pages
        # for pagename_fs in source.list_pages():

        #     body = source.get_adaptor(request, pagename_fs).get_body()

        #     pagename_fs = pagename_fs.replace('(3f)', '') #? -> ''
        #     print pagename_fs
        #     target.get_adaptor(request, pagename_fs).is_write_file(body)

