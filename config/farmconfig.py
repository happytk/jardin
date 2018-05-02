from MoinMoin.config.multiconfig import DefaultConfig
from MoinMoin.storage import (
    GitMiddleware,
    MoinWikiMiddleware,
)
from collections import OrderedDict
import sys
import os
import re

wiki_basedir = os.path.split(os.path.abspath(os.path.basename(__file__)))[0]
wiki_baseurl = r"^(http|https)://([A-Za-z0-9\-\.]+)(:[0-9]+)?/{}/.*$"
wikis = [
    (wiki, wiki_baseurl.format(wiki[5:]))
    for wiki in (
        'wiki_cph',
        'wiki_test',
    )
]

_RE_ALL = re.compile(r'.*')

class FarmConfig(DefaultConfig):

    wikiconfig_dir = os.path.dirname(__file__)

    middlewares = {'wiki': (MoinWikiMiddleware, (),),}
    routes = OrderedDict()
    routes[_RE_ALL] = 'wiki'

    url_prefix_static = '/moin_static195'
    page_credits = [
        'copyrights@2001-2017 all rights reserved.',
    ]
    page_credits.extend(['<a href="/%s">%s</a>' % (name[5:], name[5:].upper()) for name, url in wikis])

    superuser = [u"HappyTk", ]

    # IMPORTANT: grant yourself admin rights! replace YourName with
    # your user name. See HelpOnAccessControlLists for more help.
    # All acl_rights_xxx options must use unicode [Unicode]
    acl_rights_before = u"HappyTk:read,write,delete,revert,admin"

    DesktopEdition = False # give all local users full powers
    acl_rights_default = u"All:"
    surge_action_limits = None # no surge protection
    sitename = u'zee'
    logo_string = u''
    show_interwiki = 1

    # ^^^ DON'T TOUCH THIS EXCEPT IF YOU KNOW WHAT YOU DO ^^^

    # Add your configuration items here.
    secrets = 'jelkajslekfjhlakwjheflkjashdlkfueh,ajshdjfhjebajsdhf831!@#!'
    tz_offset = 9.0
    show_timings = False
    show_version = False
    supplementation_page = False
    xapian_search = False
    xapian_index_history = False
    xapian_index_dir = None
    xapian_stemming = False
    surge_action_limits = None

    cookie_name = sitename  # cookie name is same for all wikis
    cache_dir = os.path.join(wiki_basedir, 'farmdata', 'cache')
    session_dir = os.path.join(wiki_basedir, 'farmdata', 'cache', '__session__')
    user_dir = os.path.join(wiki_basedir, 'farmdata', 'user')
    plugin_dir = os.path.join(wiki_basedir, 'lib', 'MoinMoinPlugin')
