#-*-encoding:utf-8-*-
import os
from farmconfig import FarmConfig
from MoinMoin.storage import (
    GitMiddleware,
    MoinWikiMiddleware,
)

class Config(FarmConfig): #multiconfig.DefaultConfig):
# class Config(multiconfig.DefaultConfig):
    # Critical setup  ---------------------------------------------------

    # We assume that this config file is located in the instance directory, like:
    # instance_dir/
    #              wikiconfig.py
    #              data/
    #              underlay/
    # If that's not true, feel free to just set instance_dir to the real path
    # where data/ and underlay/ is located:
    #instance_dir = '/where/ever/your/instance/is'
    config_name = os.path.splitext(os.path.basename(__file__))[0]
    instance_dir = os.path.abspath(os.path.dirname(__file__)) + '/' + config_name

    # Where your own wiki pages are (make regular backups of this directory):
    data_dir = os.path.join(instance_dir, 'data', '') # path with trailing /

    middlewares = {
        'wiki': (GitMiddleware, (
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)), 
                '{0}.git'.format(config_name)),
            ),),
        # 'wiki': (MoinWikiMiddleware, (),),
    }

    # Where system and help pages are (you may exclude this from backup):
    data_underlay_dir = os.path.join(instance_dir, 'underlay', '') # path with trailing /

    # Wiki identity ----------------------------------------------------

    # Site name, used by default for wiki name-logo [Unicode]
    sitename = config_name[5:]
    interwikiname = sitename

    # Wiki logo. You can use an image, text or both. [Unicode]
    # For no logo or text, use '' - the default is to show the sitename.
    # See also url_prefix setting below!
    logo_string = u''#<img src="%s/common/moinmoin.png" alt="MoinMoin Logo">' % url_prefix_static

    # name of entry page / front page [Unicode], choose one of those:

    # a) if most wiki content is in a single language
    #page_front_page = u"MyStartingPage"

    # b) if wiki content is maintained in many languages
    page_front_page = u"FrontPage"

    # The interwiki name used in interwiki links
    #interwikiname = u'UntitledWiki'
    # Show the interwiki name (and link it to page_front_page) in the Theme,
    # nice for farm setups or when your logo does not show the wiki's name.
    # show_interwiki = 1

    # attachment_charset = 'utf-8'

    # Security ----------------------------------------------------------

    # This is checked by some rather critical and potentially harmful actions,
    # like despam or PackageInstaller action:
    # superuser = [u"HappyTk", u"MeiDay"] 

    # IMPORTANT: grant yourself admin rights! replace YourName with
    # your user name. See HelpOnAccessControlLists for more help.
    # All acl_rights_xxx options must use unicode [Unicode]
    # acl_rights_before = u"HappyTk:read,write,delete,revert,admin MeiDay:read,write,delete,revert,admin"
    # acl_rights_default = u"All:"

    # The default (ENABLED) password_checker will keep users from choosing too
    # short or too easy passwords. If you don't like this and your site has
    # rather low security requirements, feel free to DISABLE the checker by:
    #password_checker = None # None means "don't do any password strength checks"

    # Link spam protection for public wikis (Uncomment to enable)
    # Needs a reliable internet connection.
    #from MoinMoin.security.antispam import SecurityPolicy


    # Mail --------------------------------------------------------------

    # Configure to enable subscribing to pages (disabled by default)
    # or sending forgotten passwords.

    # SMTP server, e.g. "mail.provider.com" (None to disable mail)
    #mail_smarthost = ""

    # The return address, e.g u"J?gen Wiki <noreply@mywiki.org>" [Unicode]
    #mail_from = u""

    # "user pwd" if you need to use SMTP AUTH
    #mail_login = ""


    # User interface ----------------------------------------------------

    # Add your wikis important pages at the end. It is not recommended to
    # remove the default links.  Leave room for user links - don't use
    # more than 6 short items.
    # You MUST use Unicode strings here, but you need not use localized
    # page names for system and help pages, those will be used automatically
    # according to the user selected language. [Unicode]
    navi_bar = [
        # If you want to show your page_front_page here:
        u'%(page_front_page)s',
        u'RecentChanges',
        # u'FindPage',
        #u'HelpContents',
        #u'LifeJournal/Year%dW%02d' % datetime.date.today().isocalendar()[:2],
    ]

    # The default theme anonymous or new users get
    # theme_default = 'modernized'


    # Language options --------------------------------------------------

    # See http://moinmo.in/ConfigMarket for configuration in
    # YOUR language that other people contributed.

    # The main wiki language, set the direction of the wiki pages
    language_default = 'en'

    # the following regexes should match the complete name when used in free text
    # the group 'all' shall match all, while the group 'key' shall match the key only
    # e.g. CategoryFoo -> group 'all' ==  CategoryFoo, group 'key' == Foo
    # moin's code will add ^ / $ at beginning / end when needed
    # You must use Unicode strings here [Unicode]
    page_category_regex = ur'(?P<all>Category(?P<key>(?!Template)\S+))'
    # page_category_regex = ur'(?P<all>(?P<key>\S+)(분류|지도))'
    page_dict_regex = ur'(?P<all>(?P<key>\S+)Dict)'
    page_group_regex = ur'(?P<all>(?P<key>\S+)Group)'
    page_template_regex = ur'(?P<all>(?P<key>\S+)Template)'

    # Content options ---------------------------------------------------

    # Show users hostnames in RecentChanges
    show_hosts = 0

    # Enable graphical charts, requires gdchart.
    chart_options = {'width': 600, 'height': 300}
