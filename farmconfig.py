wikis = [
    ("wiki_cph",   r"^(http|https)://([0-9a-z\.]+)(:[0-9]+)?/cph/.*$"),
    ("wiki_hsk",   r"^(http|https)://([0-9a-z\.]+)(:[0-9]+)?/hsk/.*$"),
    ("wiki_got",   r"^(http|https)://([0-9a-z\.]+)(:[0-9]+)?/got/.*$"),
    ("wiki_sth",   r"^(http|https)://([0-9a-z\.]+)(:[0-9]+)?/sth/.*$"),
    ("wiki_test",  r"^(http|https)://([0-9a-z\.]+)(:[0-9]+)?/test/.*$"),
    # ("wiki_wecanfly",  r"^(http|https)://([0-9a-z\.]+)(:[0-9]+)?/wecanfly/.*$"),
    ("wiki_mei",   r"^(http|https)://([0-9a-z\.]+)(:[0-9]+)?/mei/.*$"),
    # ("wiki_erc",   r"^(http|https)://([0-9a-z\.]+)(:[0-9]+)?/erc/.*$"),
    # ("wiki_master",  r"^(http|https)://(localhost|wecanfly.net|192.168.0.4)(:[0-9]+)?/master/.*$"),
    # ("wiki_friends",  r"^(http|https)://(localhost|wecanfly.net|192.168.0.4)(:[0-9]+)?/amb/.*$"),
]

import sys
import os

MOINPATH = os.environ['MOIN']
sys.path.insert(0, MOINPATH)
sys.path.insert(0, os.path.join(MOINPATH, 'support'))
sys.path.insert(0, os.path.join(MOINPATH, 'MoinMoin', 'support'))

from MoinMoin.config.multiconfig import DefaultConfig
from MoinMoin.storage import (
    GitMiddleware,
    MoinWikiMiddleware,
)
from collections import OrderedDict
import re
_RE_ALL = re.compile(r'.*')

class FarmConfig(DefaultConfig):
    # data_underlay_dir = '/volume1/wcfdev/wiki-apt/underlay'
    #url_prefix_static = '/wikifarm'
    # theme_default = 'modernized_mobile'

    sqlrun_dbconns = {'xe': 'system/oracle@localhost:1521/xe'}

    wikiconfig_dir = os.path.dirname(__file__)

    middlewares = {'wiki': (MoinWikiMiddleware, (),),}
    routes = OrderedDict()
    routes[_RE_ALL] = 'wiki'

    url_prefix_static = '/moin_static195'
    page_credits = [
        'copyrights@2001-2016 all rights reserved.',
    ]
    page_credits.extend(['<a href="/%s">%s</a>' % (name[5:], name[5:].upper()) for name, url in wikis])

    superuser = [u"HappyTk", ]

    # IMPORTANT: grant yourself admin rights! replace YourName with
    # your user name. See HelpOnAccessControlLists for more help.
    # All acl_rights_xxx options must use unicode [Unicode]
    acl_rights_before = u"HappyTk:read,write,delete,revert,admin"

    DesktopEdition = True # give all local users full powers
    acl_rights_default = u"All:read,write,delete,revert,admin"
    surge_action_limits = None # no surge protection
    sitename = u'MoinMoin DesktopEdition'
    # logo_string = u'<img src="%s/common/moinmoin.png" alt="MoinMoin Logo">' % url_prefix_static
    logo_string = u''
    show_interwiki = 1

    # ^^^ DON'T TOUCH THIS EXCEPT IF YOU KNOW WHAT YOU DO ^^^

    #page_front_page = u'FrontPage' # change to some better value

    # Add your configuration items here.
    secrets = 'This string is NOT a secret, please make up your own, long, random secret string!'
    plugin_dir = '/Users/happytk/Dev/moin/lib/MoinMoinPlugin'
    tz_offset = 9.0
    show_timings = False
    show_version = False
    supplementation_page = False
    xapian_search = False
    xapian_index_history = False
    xapian_index_dir = None
    xapian_stemming = False
    surge_action_limits = None

    webfont_default = 'HoonSlimskinnyLWeb.woff'
    mobile_webfont_default = 'HoonSlimskinnyLWeb.woff'
    # default_markup = 'text_markdown'
