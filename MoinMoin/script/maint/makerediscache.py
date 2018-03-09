# -*- coding: utf-8 -*-
"""
MoinMoin - build redis cache

@copyright: 2004-2006 MoinMoin:ThomasWaldmann
@license: GNU GPL, see COPYING for details.
"""

debug = False

from MoinMoin.script import MoinScript
from MoinMoin.dayone_multi import DayoneMiddleware

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
        self.parser.add_option(
            "--empty", action="store_true", dest="empty",
            help="remove all caches"
        )

    def mainloop(self):
        self.init_request()
        request = self.request

        print len(request.cfg.redis.keys())
        for storage in request.storage.values():
            if isinstance(storage, DayoneMiddleware):
                print storage.prefix
                storage.refresh_redis(request.cfg.redis, empty=self.options.empty)
        print len(request.cfg.redis.keys())
