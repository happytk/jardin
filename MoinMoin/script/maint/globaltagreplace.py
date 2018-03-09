# -*- coding: utf-8 -*-
"""
MoinMoin - build redis cache

@copyright: 2004-2006 MoinMoin:ThomasWaldmann
@license: GNU GPL, see COPYING for details.
"""

debug = False

from MoinMoin.script import MoinScript
from MoinMoin.dayone_multi import DayoneMiddleware, Entry
import re

class PluginScript(MoinScript):
    """\
Purpose:
========
This tool allows you to list up all the pages in a wiki.

Detailed Instructions:
======================
General syntax: moin [options] maint globaltagreplace

[options] usually should be:
    --config-dir=/path/to/my/cfg/ --wiki-url=http://wiki.example.org/

"""

    def __init__(self, argv, def_values):
        MoinScript.__init__(self, argv, def_values)

        self.parser.add_option(
            "--fr", metavar="FR", dest="fr",
            help="original tag name"
        )
        self.parser.add_option(
            "--to", metavar="TO", dest="to",
            help="replace tag name"
        )
        self.parser.add_option(
            "--test", action="store_true", dest="test",
            help="test (will be not saved.)"
        )

    def mainloop(self):
        self.init_request()
        request = self.request

        for storage in request.storage.values():
            if isinstance(storage, DayoneMiddleware):
                entries = map(lambda x: Entry(storage, x), storage._list_files(request))
                for entry in entries:
                    if entry.has_tag(self.options.fr):
                        entry.rmtag(self.options.fr)
                        entry.addtag(self.options.to)
                        regex = r'#(%s)([^\w]*)' % self.options.fr
                        replace_text = re.sub(regex, r'#%s\2' % self.options.to, entry.text)
                        if self.options.test:
                            print replace_text
                        else:
                            entry.text = replace_text
                            entry.save()
                            print entry.filename