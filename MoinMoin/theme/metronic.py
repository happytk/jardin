# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - Theme Package

    @copyright: 2003-2008 MoinMoin:ThomasWaldmann
    @license: GNU GPL, see COPYING for details.
"""

import StringIO

from MoinMoin import log
logging = log.getLogger(__name__)

from MoinMoin import i18n, wikiutil, config, version, caching
from MoinMoin.action import get_available_actions
from MoinMoin.Page import Page
from MoinMoin.util import pysupport

from MoinMoin.theme import ThemeBase
from MoinMoin import wikiutil
from MoinMoin.Page import Page


class Theme(ThemeBase):
    """ Base class for themes

    This class supply all the standard template that sub classes can
    use without rewriting the same code. If you want to change certain
    elements, override them.
    """

    name = 'metronic'

    # fake _ function to get gettext recognize those texts:
    _ = lambda x: x

    # TODO: remove icons that are not used any more.
    icons = {
        # key         alt                        icon filename      w   h
        # ------------------------------------------------------------------
        # navibar
        'help':        ("%(page_help_contents)s", "moin-help.png",   12, 11),
        'find':        ("%(page_find_page)s",     "moin-search.png", 12, 12),
        'diff':        (_("Diffs"),               "moin-diff.png",   15, 11),
        'info':        (_("Info"),                "moin-info.png",   12, 11),
        'edit':        (_("Edit"),                "moin-edit.png",   12, 12),
        'unsubscribe': (_("Unsubscribe"),         "moin-unsubscribe.png", 14, 10),
        'subscribe':   (_("Subscribe"),           "moin-subscribe.png", 14, 10),
        'raw':         (_("Raw"),                 "moin-raw.png",    12, 13),
        'xml':         (_("XML"),                 "moin-xml.png",    20, 13),
        'print':       (_("Print"),               "moin-print.png",  16, 14),
        'view':        (_("View"),                "moin-show.png",   12, 13),
        'home':        (_("Home"),                "moin-home.png",   13, 12),
        'up':          (_("Up"),                  "moin-parent.png", 15, 13),
        # FileAttach
        'attach':     ("%(attach_count)s",       "moin-attach.png",  7, 15),
        'attachimg':  ("",                       "attach.png",      32, 32),
        # RecentChanges
        'rss':        (_("[RSS]"),               "moin-rss.png",    24, 24),
        'deleted':    (_("[DELETED]"),           "moin-deleted.png", 60, 12),
        'updated':    (_("[UPDATED]"),           "moin-updated.png", 60, 12),
        'renamed':    (_("[RENAMED]"),           "moin-renamed.png", 60, 12),
        'conflict':   (_("[CONFLICT]"),          "moin-conflict.png", 60, 12),
        'new':        (_("[NEW]"),               "moin-new.png",    31, 12),
        'diffrc':     (_("[DIFF]"),              "moin-diff.png",   15, 11),
        # General
        'bottom':     (_("[BOTTOM]"),            "moin-bottom.png", 14, 10),
        'top':        (_("[TOP]"),               "moin-top.png",    14, 10),
        'www':        ("[WWW]",                  "moin-www.png",    11, 11),
        'mailto':     ("[MAILTO]",               "moin-email.png",  14, 10),
        'news':       ("[NEWS]",                 "moin-news.png",   10, 11),
        'telnet':     ("[TELNET]",               "moin-telnet.png", 10, 11),
        'ftp':        ("[FTP]",                  "moin-ftp.png",    11, 11),
        'file':       ("[FILE]",                 "moin-ftp.png",    11, 11),
        # search forms
        'searchbutton': ("[?]",                  "moin-search.png", 12, 12),
        'interwiki':  ("[%(wikitag)s]",          "moin-inter.png",  16, 16),

        # smileys (this is CONTENT, but good looking smileys depend on looking
        # adapted to the theme background color and theme style in general)
        #vvv    ==      vvv  this must be the same for GUI editor converter
        'X-(':        ("X-(",                    'angry.png',       15, 15),
        ':D':         (":D",                     'biggrin.png',     15, 15),
        '<:(':        ("<:(",                    'frown.png',       15, 15),
        ':o':         (":o",                     'redface.png',     15, 15),
        ':(':         (":(",                     'sad.png',         15, 15),
        ':)':         (":)",                     'smile.png',       15, 15),
        'B)':         ("B)",                     'smile2.png',      15, 15),
        ':))':        (":))",                    'smile3.png',      15, 15),
        ';)':         (";)",                     'smile4.png',      15, 15),
        '/!\\':       ("/!\\",                   'alert.png',       15, 15),
        '<!>':        ("<!>",                    'attention.png',   15, 15),
        '(!)':        ("(!)",                    'idea.png',        15, 15),

        # copied 2001-11-16 from http://pikie.darktech.org/cgi/pikie.py?EmotIcon
        ':-?':        (":-?",                    'tongue.png',      15, 15),
        ':\\':        (":\\",                    'ohwell.png',      15, 15),
        '>:>':        (">:>",                    'devil.png',       15, 15),
        '|)':         ("|)",                     'tired.png',       15, 15),

        # some folks use noses in their emoticons
        ':-(':        (":-(",                    'sad.png',         15, 15),
        ':-)':        (":-)",                    'smile.png',       15, 15),
        'B-)':        ("B-)",                    'smile2.png',      15, 15),
        ':-))':       (":-))",                   'smile3.png',      15, 15),
        ';-)':        (";-)",                    'smile4.png',      15, 15),
        '|-)':        ("|-)",                    'tired.png',       15, 15),

        # version 1.0
        '(./)':       ("(./)",                   'checkmark.png',   20, 15),
        '{OK}':       ("{OK}",                   'thumbs-up.png',   14, 12),
        '{X}':        ("{X}",                    'icon-error.png',  16, 16),
        '{i}':        ("{i}",                    'icon-info.png',   16, 16),
        '{1}':        ("{1}",                    'prio1.png',       15, 13),
        '{2}':        ("{2}",                    'prio2.png',       15, 13),
        '{3}':        ("{3}",                    'prio3.png',       15, 13),

        # version 1.3.4 (stars)
        # try {*}{*}{o}
        '{*}':        ("{*}",                    'star_on.png',     15, 15),
        '{o}':        ("{o}",                    'star_off.png',    15, 15),
    }
    del _

    # Style sheets - usually there is no need to override this in sub
    # classes. Simply supply the css files in the css directory.

    # Standard set of style sheets
    stylesheets = (
        # media         basename
        ('all',         'common'),
        ('screen',      'screen'),
        ('print',       'print'),
        ('projection',  'projection'),
        )

    # Used in print mode
    stylesheets_print = (
        # media         basename
        ('all',         'common'),
        ('all',         'print'),
        )

    # Used in slide show mode
    stylesheets_projection = (
        # media         basename
        ('all',         'common'),
        ('all',         'projection'),
       )

    stylesheetsCharset = 'utf-8'

    def __init__(self, request):
        """
        Initialize the theme object.

        @param request: the request object
        """
        self.request = request
        self.cfg = request.cfg
        self._cache = {} # Used to cache elements that may be used several times
        self._status = []
        self._send_title_called = False

    def img_url(self, img):
        """ Generate an image href

        @param img: the image filename
        @rtype: string
        @return: the image href
        """
        return "%s/%s/img/%s" % (self.cfg.url_prefix_static, self.name, img)

    def emit_custom_html(self, html):
        """
        generate custom HTML code in `html`

        @param html: a string or a callable object, in which case
                     it is called and its return value is used
        @rtype: string
        @return: string with html
        """
        if html:
            if callable(html):
                html = html(self.request)
        return html

    def logo(self):
        """ Assemble logo with link to front page

        The logo contain an image and or text or any html markup the
        admin inserted in the config file. Everything it enclosed inside
        a div with id="logo".

        @rtype: unicode
        @return: logo html
        """
        html = u''
        if self.cfg.logo_string:
            page = wikiutil.getFrontPage(self.request)
            logo = page.link_to_raw(self.request, self.cfg.logo_string)
            # html = u'''<div id="logo">%s</div>''' % logo
            html = logo
        return html

    def interwiki(self, d):
        """ Assemble the interwiki name display, linking to page_front_page

        @param d: parameter dictionary
        @rtype: string
        @return: interwiki html
        """
        if self.request.cfg.show_interwiki:
            page = wikiutil.getFrontPage(self.request)
            text = self.request.cfg.interwikiname or u'Self'
            link = page.link_to(self.request, text=text, rel='nofollow')
            html = u'<div id="interwiki"><span>%s</span></div>' % link
        else:
            html = u''
        return html

    def title(self, d):
        """ Assemble the title (now using breadcrumbs)

        @param d: parameter dictionary
        @rtype: string
        @return: title html
        """
        _ = self.request.getText
        content = []
        if d['title_text'] == d['page'].split_title(): # just showing a page, no action
            curpage = ''
            segments = d['page_name'].split('/') # was: title_text
            for s in segments[:-1]:
                curpage += s
                content.append("<li>%s</li>" % Page(self.request, curpage).link_to(self.request, s))
                curpage += '/'
            link_text = segments[-1]
            link_title = _('Click to do a full-text search for this title')
            link_query = {
                'action': 'fullsearch',
                'value': 'linkto:"%s"' % d['page_name'],
                'context': '180',
            }
            # we dont use d['title_link'] any more, but make it ourselves:
            link = d['page'].link_to(self.request, link_text, querystr=link_query, title=link_title, css_class='backlink', rel='nofollow')
            content.append(('<li>%s</li>') % link)
        else:
            content.append('<li>%s</li>' % wikiutil.escape(d['title_text']))

        html = '''
<ul id="pagelocation">
%s
</ul>
''' % "".join(content)
        return html

    def title_with_separators(self, d):
        """ Assemble the title using slashes, not <ul>

        @param d: parameter dictionary
        @rtype: string
        @return: title html
        """
        _ = self.request.getText
        if d['title_text'] == d['page'].split_title():
            # just showing a page, no action
            segments = d['page_name'].split('/')
            link_text = segments[-1]
            link_title = _('Click to do a full-text search for this title')
            link_query = {'action': 'fullsearch', 'context': '180',
                          'value': 'linkto:"%s"' % d['page_name'], }
            link = d['page'].link_to(self.request, link_text,
                                     querystr=link_query, title=link_title,
                                     css_class='backlink', rel='nofollow')
            if len(segments) <= 1:
                html = link
            else:
                content = []
                curpage = ''
                for s in segments[:-1]:
                    curpage += s
                    content.append(Page(self.request,
                                        curpage).link_to(self.request, s))
                    curpage += '/'
                path_html = u'<span class="sep">/</span>'.join(content)
                html = u'<span class="pagepath">%s</span><span class="sep">/</span>%s' % (path_html, link)
        else:
            html = wikiutil.escape(d['title_text'])
        return u'<span id="pagelocation">%s</span>' % html

    def username(self, d):
        """ Assemble the username / userprefs link

        @param d: parameter dictionary
        @rtype: unicode
        @return: username html
        """
        request = self.request
        _ = request.getText

        userlinks = []
        # Add username/homepage link for registered users. We don't care
        # if it exists, the user can create it.
        if request.user.valid and request.user.name:
            interwiki = wikiutil.getInterwikiHomePage(request)
            name = request.user.name
            aliasname = request.user.aliasname
            if not aliasname:
                aliasname = name
            title = "%s @ %s" % (aliasname, interwiki[0])
            # link to (interwiki) user homepage
            homelink = (request.formatter.interwikilink(1, title=title, id="userhome", generated=True, *interwiki) +
                        request.formatter.text(name) +
                        request.formatter.interwikilink(0, title=title, id="userhome", *interwiki))
            userlinks.append(homelink)
            # link to userprefs action
            if 'userprefs' not in self.request.cfg.actions_excluded:
                userlinks.append(d['page'].link_to(request, text=_('Settings'),
                                               querystr={'action': 'userprefs'}, id='userprefs', rel='nofollow'))

        if request.user.valid:
            if request.user.auth_method in request.cfg.auth_can_logout:
                userlinks.append(d['page'].link_to(request, text=_('Logout'),
                                                   querystr={'action': 'logout', 'logout': 'logout'}, id='logout', rel='nofollow'))
        else:
            query = {'action': 'login'}
            # special direct-login link if the auth methods want no input
            if request.cfg.auth_login_inputs == ['special_no_input']:
                query['login'] = '1'
            if request.cfg.auth_have_login:
                userlinks.append(d['page'].link_to(request, text=_("Login"),
                                                   querystr=query, id='login', rel='nofollow'))

        userlinks = [u'<li>%s</li>' % link for link in userlinks]
        html = u'<ul id="username">%s</ul>' % ''.join(userlinks)
        return html

    def splitNavilink(self, text, localize=1):
        """ Split navibar links into pagename, link to page

        Admin or user might want to use shorter navibar items by using
        the [[page|title]] or [[url|title]] syntax. In this case, we don't
        use localization, and the links goes to page or to the url, not
        the localized version of page.

        Supported syntax:
            * PageName
            * WikiName:PageName
            * wiki:WikiName:PageName
            * url
            * all targets as seen above with title: [[target|title]]

        @param text: the text used in config or user preferences
        @rtype: tuple
        @return: pagename or url, link to page or url
        """
        request = self.request
        fmt = request.formatter
        title = None

        # Handle [[pagename|title]] or [[url|title]] formats
        if text.startswith('[[') and text.endswith(']]'):
            text = text[2:-2]
            try:
                pagename, title = text.split('|', 1)
                pagename = pagename.strip()
                title = title.strip()
                localize = 0
            except (ValueError, TypeError):
                # Just use the text as is.
                pagename = text.strip()
        else:
            pagename = text

        if wikiutil.is_URL(pagename):
            if not title:
                title = pagename
            link = fmt.url(1, pagename) + fmt.text(title) + fmt.url(0)
            return pagename, link

        # remove wiki: url prefix
        if pagename.startswith("wiki:"):
            pagename = pagename[5:]

        # try handling interwiki links
        try:
            interwiki, page = wikiutil.split_interwiki(pagename)
            thiswiki = request.cfg.interwikiname
            if interwiki == thiswiki or interwiki == 'Self':
                pagename = page
            else:
                if not title:
                    title = page
                link = fmt.interwikilink(True, interwiki, page) + fmt.text(title) + fmt.interwikilink(False, interwiki, page)
                return pagename, link
        except ValueError:
            pass

        # Handle regular pagename like "FrontPage"
        pagename = wikiutil.normalize_pagename(pagename, request.cfg)

        # Use localized pages for the current user
        if localize:
            page = wikiutil.getLocalizedPage(request, pagename)
        else:
            page = Page(request, pagename)

        pagename = page.page_name # can be different, due to i18n

        if not title:
            title = page.split_title()
            title = self.shortenPagename(title)

        link = page.link_to(request, title)

        return pagename, link

    def shortenPagename(self, name):
        """ Shorten page names

        Shorten very long page names that tend to break the user
        interface. The short name is usually fine, unless really stupid
        long names are used (WYGIWYD).

        If you don't like to do this in your theme, or want to use
        different algorithm, override this method.

        @param name: page name, unicode
        @rtype: unicode
        @return: shortened version.
        """
        maxLength = self.maxPagenameLength()
        # First use only the sub page name, that might be enough
        if len(name) > maxLength:
            name = name.split('/')[-1]
            # If it's not enough, replace the middle with '...'
            if len(name) > maxLength:
                half, left = divmod(maxLength - 3, 2)
                name = u'%s...%s' % (name[:half + left], name[-half:])
        return name

    def maxPagenameLength(self):
        """ Return maximum length for shortened page names """
        return 25

    def navibar(self, d):
        """ Assemble the navibar

        @param d: parameter dictionary
        @rtype: unicode
        @return: navibar html
        """
        request = self.request
        found = {} # pages we found. prevent duplicates
        items = [] # navibar items
        item = u'<li class="%s">%s</li>'
        current = d['page_name']

        # Process config navi_bar
        if request.cfg.navi_bar:
            for text in request.cfg.navi_bar:
                pagename, link = self.splitNavilink(text)
                if pagename == current:
                    cls = 'wikilink current'
                else:
                    cls = 'wikilink'
                items.append(item % (cls, link))
                found[pagename] = 1

        # Add user links to wiki links, eliminating duplicates.
        userlinks = request.user.getQuickLinks()
        for text in userlinks:
            # Split text without localization, user knows what he wants
            pagename, link = self.splitNavilink(text, localize=0)
            if not pagename in found:
                if pagename == current:
                    cls = 'userlink current'
                else:
                    cls = 'userlink'
                items.append(item % (cls, link))
                found[pagename] = 1

        # Add current page at end of local pages
        if not current in found:
            title = d['page'].split_title()
            title = self.shortenPagename(title)
            link = d['page'].link_to(request, title)
            cls = 'current'
            items.append(item % (cls, link))

        # Add sister pages.
        for sistername, sisterurl in request.cfg.sistersites:
            if sistername == request.cfg.interwikiname: # it is THIS wiki
                cls = 'sisterwiki current'
                items.append(item % (cls, sistername))
            else:
                # TODO optimize performance
                cache = caching.CacheEntry(request, 'sisters', sistername, 'farm', use_pickle=True)
                if cache.exists():
                    data = cache.content()
                    sisterpages = data['sisterpages']
                    if current in sisterpages:
                        cls = 'sisterwiki'
                        url = sisterpages[current]
                        link = request.formatter.url(1, url) + \
                               request.formatter.text(sistername) +\
                               request.formatter.url(0)
                        items.append(item % (cls, link))

        # Assemble html
        items = u''.join(items)
        html = u'''
<ul id="navibar">
%s
</ul>
''' % items
        return html

    def get_icon(self, icon):
        """ Return icon data from self.icons

        If called from <<Icon(file)>> we have a filename, not a
        key. Using filenames is deprecated, but for now, we simulate old
        behavior.

        @param icon: icon name or file name (string)
        @rtype: tuple
        @return: alt (unicode), href (string), width, height (int)
        """
        if icon in self.icons:
            alt, icon, w, h = self.icons[icon]
        else:
            # Create filenames to icon data mapping on first call, then
            # cache in class for next calls.
            if not getattr(self.__class__, 'iconsByFile', None):
                d = {}
                for data in self.icons.values():
                    d[data[1]] = data
                self.__class__.iconsByFile = d

            # Try to get icon data by file name
            if icon in self.iconsByFile:
                alt, icon, w, h = self.iconsByFile[icon]
            else:
                alt, icon, w, h = '', icon, '', ''

        return alt, self.img_url(icon), w, h

    def make_icon(self, icon, vars=None, **kw):
        """
        This is the central routine for making <img> tags for icons!
        All icons stuff except the top left logo and search field icons are
        handled here.

        @param icon: icon id (dict key)
        @param vars: ...
        @rtype: string
        @return: icon html (img tag)
        """
        if vars is None:
            vars = {}
        alt, img, w, h = self.get_icon(icon)
        try:
            alt = vars['icon-alt-text'] # if it is possible we take the alt-text from 'page_icons_table'
        except KeyError, err:
            try:
                alt = alt % vars # if not we just leave the  alt-text from 'icons'
            except KeyError, err:
                alt = 'KeyError: %s' % str(err)
        alt = self.request.getText(alt)
        tag = self.request.formatter.image(src=img, alt=alt, width=w, height=h, **kw)
        return tag

    def make_iconlink(self, which, d):
        """
        Make a link with an icon

        @param which: icon id (dictionary key)
        @param d: parameter dictionary
        @rtype: string
        @return: html link tag
        """
        qs = {}
        pagekey, querystr, title, icon = self.cfg.page_icons_table[which]
        qs.update(querystr) # do not modify the querystr dict in the cfg!
        d['icon-alt-text'] = d['title'] = title % d
        d['i18ntitle'] = self.request.getText(d['title'])
        img_src = self.make_icon(icon, d)
        rev = d['rev']
        if rev and which in ['raw', 'print', ]:
            qs['rev'] = str(rev)
        attrs = {'rel': 'nofollow', 'title': d['i18ntitle'], }
        page = d[pagekey]
        if isinstance(page, unicode):
            # e.g. d['page_parent_page'] is just the unicode pagename
            # while d['page'] will give a page object
            page = Page(self.request, page)
        return page.link_to_raw(self.request, text=img_src, querystr=qs, **attrs)

    def msg(self, d):
        """ Assemble the msg display

        Display a message with a widget or simple strings with a clear message link.

        @param d: parameter dictionary
        @rtype: unicode
        @return: msg display html
        """
        _ = self.request.getText
        msgs = d['msg']

        result = u""
        close = d['page'].link_to(self.request, text=_('Clear message'), css_class="clear-link")
        for msg, msg_class in msgs:
            try:
                result += u'<p>%s</p>' % msg.render()
                close = ''
            except AttributeError:
                if msg and msg_class:
                    result += u'<p><div class="%s">%s</div></p>' % (msg_class, msg)
                elif msg:
                    result += u'<p>%s</p>\n' % msg
        if result:
            html = result + close
            return u'<div id="message">\n%s\n</div>\n' % html
        else:
            return u''

        return u'<div id="message">\n%s\n</div>\n' % html

    def trail(self, d):
        """ Assemble page trail

        @param d: parameter dictionary
        @rtype: unicode
        @return: trail html
        """
        request = self.request
        user = request.user
        html = ''
        if not user.valid or user.show_page_trail:
            trail = user.getTrail()
            if trail:
                items = []
                for pagename in trail:
                    try:
                        interwiki, page = wikiutil.split_interwiki(pagename)
                        if interwiki != request.cfg.interwikiname and interwiki != 'Self':
                            link = (self.request.formatter.interwikilink(True, interwiki, page) +
                                    self.shortenPagename(page) +
                                    self.request.formatter.interwikilink(False, interwiki, page))
                            items.append('<li>%s</li>' % link)
                            continue
                        else:
                            pagename = page

                    except ValueError:
                        pass
                    page = Page(request, pagename)
                    title = page.split_title()
                    title = self.shortenPagename(title)
                    link = page.link_to(request, title)
                    items.append('<li>%s</li>' % link)
                html = '''
<ul id="pagetrail">
%s
</ul>''' % ''.join(items)
        return html

    def _stylesheet_link(self, theme, media, href, title=None):
        """
        Create a link tag for a stylesheet.

        @param theme: True: href gives the basename of a theme stylesheet,
                      False: href is a full url of a user/admin defined stylesheet.
        @param media: 'all', 'screen', 'print', 'projection', ...
        @param href: see param theme
        @param title: optional title (for alternate stylesheets), see
                      http://www.w3.org/Style/Examples/007/alternatives
        @rtype: string
        @return: stylesheet link html
        """
        if theme:
            href = '%s/%s/css/%s.css' % (self.cfg.url_prefix_static, self.name, href)
        attrs = 'type="text/css" charset="%s" media="%s" href="%s"' % (
                self.stylesheetsCharset, media, href, )
        if title:
            return '<link rel="alternate stylesheet" %s title="%s">' % (attrs, title)
        else:
            return '<link rel="stylesheet" %s>' % attrs

    def html_stylesheets(self, d):
        """ Assemble html head stylesheet links

        @param d: parameter dictionary
        @rtype: string
        @return: stylesheets links
        """
        request = self.request
        # Check mode
        if d.get('print_mode'):
            media = d.get('media', 'print')
            stylesheets = getattr(self, 'stylesheets_' + media)
        else:
            stylesheets = self.stylesheets

        theme_css = [self._stylesheet_link(True, *stylesheet) for stylesheet in stylesheets]
        cfg_css = [self._stylesheet_link(False, *stylesheet) for stylesheet in request.cfg.stylesheets]

        msie_css = """
<!-- css only for MS IE6/IE7 browsers -->
<!--[if lt IE 8]>
   %s
<![endif]-->
""" % self._stylesheet_link(True, 'all', 'msie')

        # Add user css url (assuming that user css uses same charset)
        href = request.user.valid and request.user.css_url
        if href and href.lower() != "none":
            user_css = self._stylesheet_link(False, 'all', href)
        else:
            user_css = ''

#         import re
#         is_webfont_preferred = re.search(r"android.+mobile|iphone|ipod|mac os x", request.http_user_agent, re.I|re.M) is not None
#         if is_webfont_preferred:
#             webfont_css = u'''<style type='text/css'>
# @font-face {
#     font-family: 'web-font';
#     src: url('%s/common/wf/531198f4d63c939ac15d4438ec289304db4d3a0d9ccf7668.woff');
#     font-weight: normal;
#     font-style: normal;
# }
# * { font-family: web-font, Courier New, AppleGothic !important;  }
# </style>''' % self.request.cfg.url_prefix_static
#         else:
#             webfont_css = u'''<style type='text/css'>
# @import url(https://fonts.googleapis.com/earlyaccess/nanumgothic.css);
# * { font-family: 'Comic sans ms', 'Nanum Gothic' !important; }
# #content { line-height: 160%; }
# </style>'''


#        return '\n'.join(theme_css + cfg_css + [msie_css, user_css, webfont_css])
        return '\n'.join(theme_css + cfg_css + [msie_css, user_css])


    def shouldShowPageinfo(self, page):
        """ Should we show page info?

        Should be implemented by actions. For now, we check here by action
        name and page.

        @param page: current page
        @rtype: bool
        @return: true if should show page info
        """
        if page.exists() and self.request.user.may.read(page.page_name):
            # These  actions show the  page content.
            # TODO: on new action, page info will not show.
            # A better solution will be if the action itself answer the question: showPageInfo().
            contentActions = [u'', u'show', u'refresh', u'preview', u'diff',
                              u'subscribe', u'RenamePage', u'CopyPage', u'DeletePage',
                              u'SpellCheck', u'print']
            return self.request.action in contentActions
        return False

    def pageinfo(self, page):
        """ Return html fragment with page meta data

        Since page information uses translated text, it uses the ui
        language and direction. It looks strange sometimes, but
        translated text using page direction looks worse.

        @param page: current page
        @rtype: unicode
        @return: page last edit information
        """
        _ = self.request.getText
        html = ''
        if self.shouldShowPageinfo(page):
            info = page.lastEditInfo()
            if info:
                if info['editor']:
                    info = _("last edited %(time)s by %(editor)s") % info
                else:
                    info = _("last modified %(time)s") % info
                pagename = page.page_name
                if self.request.cfg.show_interwiki:
                    pagename = "%s: %s" % (self.request.cfg.interwikiname, pagename)

                info = "%s:%s (%s)" % (wikiutil.escape(pagename), page.middleware, info)
                html = '<p id="pageinfo" class="info"%(lang)s>%(info)s</p>\n' % {
                    'lang': self.ui_lang_attr(),
                    'info': info
                    }
        return html

    def searchform(self, d):
        """
        assemble HTML code for the search forms

        @param d: parameter dictionary
        @rtype: unicode
        @return: search form html
        """
        _ = self.request.getText
        form = self.request.values
        updates = {
            'search_label': _('Search:'),
            'search_value': wikiutil.escape(form.get('value', ''), 1),
            'search_full_label': _('Text'),
            'search_title_label': _('Titles'),
            'url': self.request.href(d['page'].page_name)
            }
        d.update(updates)

        html = u'''
<form id="searchform" method="get" action="%(url)s">
<div>
<input type="hidden" name="action" value="fullsearch">
<input type="hidden" name="context" value="180">
<label for="searchinput">%(search_label)s</label>
<input id="searchinput" type="text" name="value" value="%(search_value)s" size="20"
    onfocus="searchFocus(this)" onblur="searchBlur(this)"
    onkeyup="searchChange(this)" onchange="searchChange(this)" alt="Search">
<input id="titlesearch" name="titlesearch" type="submit"
    value="%(search_title_label)s" alt="Search Titles">
<input id="fullsearch" name="fullsearch" type="submit"
    value="%(search_full_label)s" alt="Search Full Text">
</div>
</form>
<script type="text/javascript">
<!--// Initialize search form
var f = document.getElementById('searchform');
f.getElementsByTagName('label')[0].style.display = 'none';
var e = document.getElementById('searchinput');
searchChange(e);
searchBlur(e);
//-->
</script>
''' % d
        return html

    def showversion(self, d, **keywords):
        """
        assemble HTML code for copyright and version display

        @param d: parameter dictionary
        @rtype: string
        @return: copyright and version display html
        """
        html = ''
        if self.cfg.show_version and not keywords.get('print_mode', 0):
            html = (u'<div id="version">MoinMoin Release %s [Revision %s], '
                     'Copyright by Juergen Hermann et al.</div>') % (version.release, version.revision, )
        return html

    def headscript(self, d):
        """ Return html head script with common functions

        @param d: parameter dictionary
        @rtype: unicode
        @return: script for html head
        """
        # Don't add script for print view
        if self.request.action == 'print':
            return u''

        _ = self.request.getText
        script = u"""
<script type="text/javascript">
<!--
var search_hint = "%(search_hint)s";
//-->
</script>
""" % {
    'search_hint': _('Search'),
    }
        return script


    def rsshref(self, page):
        """ Create rss href, used for rss button and head link

        @rtype: unicode
        @return: rss href
        """
        request = self.request
        url = page.url(request, querystr={
                'action': 'rss_rc', 'ddiffs': '1', 'unique': '1', }, escape=0)
        return url

    def html_head(self, d):
        """ Assemble html head

        @param d: parameter dictionary
        @rtype: unicode
        @return: html head
        """
        html = [
            u'<title>%(title)s - %(sitename)s</title>' % {
                'title': wikiutil.escape(d['title']),
                'sitename': wikiutil.escape(d['sitename']),
            },
            self.externalScript('common'),
            self.externalScript('moin'),
            '''<script>
    set_script_root('%s');
</script>''' % self.request.getScriptname(),
#             self.externalScript('audiojs/audio.min'),
#             '''<script>
#   audiojs.events.ready(function() {
#     var as = audiojs.createAll();
#   });
# </script>''',
            # self.externalScript('jquery-1.11.2.min'),
            # self.externalScript('select2.min'),
            # u'<link href="%s/common/js/select2.min.css" rel="stylesheet" />' % self.request.cfg.url_prefix_static,
            self.headscript(d), # Should move to separate .js file
            self.guiEditorScript(d),
            self.html_stylesheets(d),
            self.rsslink(d),
            self.universal_edit_button(d),
            ]
        return '\n'.join(html)

    def externalScript(self, name):
        """ Format external script html """
        src = '%s/common/js/%s.js' % (self.request.cfg.url_prefix_static, name)
        return '<script type="text/javascript" src="%s"></script>' % src

    def universal_edit_button(self, d, **keywords):
        """ Generate HTML for an edit link in the header."""
        page = d['page']
        if 'edit' in self.request.cfg.actions_excluded:
            return ""
        if not (page.isWritable() and
                self.request.user.may.write(page.page_name)):
            return ""
        _ = self.request.getText
        querystr = {'action': 'edit'}
        text = _(u'Edit')
        url = page.url(self.request, querystr=querystr, escape=0)
        return (u'<link rel="alternate" type="application/wiki" '
                u'title="%s" href="%s">' % (text, url))

    def credits(self, d, **keywords):
        """ Create credits html from credits list """
        if isinstance(self.cfg.page_credits, (list, tuple)):
            items = ['<li>%s</li>' % i for i in self.cfg.page_credits]
            html = '<ul id="credits">\n%s\n</ul>\n' % ''.join(items)
        else:
            # Old config using string, output as is
            html = self.cfg.page_credits
        return html

    def actionsMenu(self, page):
        """ Create actions menu list and items data dict

        The menu will contain the same items always, but items that are
        not available will be disabled (some broken browsers will let
        you select disabled options though).

        The menu should give best user experience for javascript
        enabled browsers, and acceptable behavior for those who prefer
        not to use Javascript.

        TODO: Move actionsMenuInit() into body onload - requires that the theme will render body,
              it is currently done in wikiutil/page.

        @param page: current page, Page object
        @rtype: unicode
        @return: actions menu html fragment
        """
        request = self.request
        _ = request.getText
        rev = request.rev

        menu = [
            'raw',
            'print',
            'RenderAsDocbook',
            'refresh',
            '__separator__',
            'SpellCheck',
            'LikePages',
            'LocalSiteMap',
            '__separator__',
            'RenamePage',
            'CopyPage',
            'DeletePage',
            '__separator__',
            'MyPages',
            'SubscribeUser',
            '__separator__',
            'Despam',
            'revert',
            'PackagePages',
            'SyncPages',
            ]

        titles = {
            # action: menu title
            '__title__': _("More Actions:"),
            # Translation may need longer or shorter separator
            '__separator__': _('------------------------'),
            'raw': _('Raw Text'),
            'print': _('Print View'),
            'refresh': _('Delete Cache'),
            'SpellCheck': _('Check Spelling'), # rename action!
            'RenamePage': _('Rename Page'),
            'CopyPage': _('Copy Page'),
            'DeletePage': _('Delete Page'),
            'LikePages': _('Like Pages'),
            'LocalSiteMap': _('Local Site Map'),
            'MyPages': _('My Pages'),
            'SubscribeUser': _('Subscribe User'),
            'Despam': _('Remove Spam'),
            'revert': _('Revert to this revision'),
            'PackagePages': _('Package Pages'),
            'RenderAsDocbook': _('Render as Docbook'),
            'SyncPages': _('Sync Pages'),
            }

        options = []
        option = '<option value="%(action)s"%(disabled)s>%(title)s</option>'
        # class="disabled" is a workaround for browsers that ignore
        # "disabled", e.g IE, Safari
        # for XHTML: data['disabled'] = ' disabled="disabled"'
        disabled = ' disabled class="disabled"'

        # Format standard actions
        available = get_available_actions(request.cfg, page, request.user)
        for action in menu:
            data = {'action': action, 'disabled': '', 'title': titles[action]}
            # removes excluded actions from the more actions menu
            if action in request.cfg.actions_excluded:
                continue

            # Enable delete cache only if page can use caching
            if action == 'refresh':
                if not page.canUseCache():
                    data['action'] = 'show'
                    data['disabled'] = disabled

            # revert action enabled only if user can revert
            if action == 'revert' and not request.user.may.revert(page.page_name):
                data['action'] = 'show'
                data['disabled'] = disabled

            # SubscribeUser action enabled only if user has admin rights
            if action == 'SubscribeUser' and not request.user.may.admin(page.page_name):
                data['action'] = 'show'
                data['disabled'] = disabled

            # Despam action enabled only for superusers
            if action == 'Despam' and not request.user.isSuperUser():
                data['action'] = 'show'
                data['disabled'] = disabled

            # Special menu items. Without javascript, executing will
            # just return to the page.
            if action.startswith('__'):
                data['action'] = 'show'

            # Actions which are not available for this wiki, user or page
            if (action == '__separator__' or
                (action[0].isupper() and not action in available)):
                data['disabled'] = disabled

            options.append(option % data)

        # Add custom actions not in the standard menu, except for
        # some actions like AttachFile (we have them on top level)
        more = [item for item in available if not item in titles and not item in ('AttachFile', )]
        more.sort()
        if more:
            # Add separator
            separator = option % {'action': 'show', 'disabled': disabled,
                                  'title': titles['__separator__']}
            options.append(separator)
            # Add more actions (all enabled)
            for action in more:
                data = {'action': action, 'disabled': ''}
                # Always add spaces: AttachFile -> Attach File
                # XXX do not create page just for using split_title -
                # creating pages for non-existent does 2 storage lookups
                #title = Page(request, action).split_title(force=1)
                title = action
                # Use translated version if available
                data['title'] = _(title)
                options.append(option % data)

        data = {
            'label': titles['__title__'],
            'options': '\n'.join(options),
            'rev_field': rev and '<input type="hidden" name="rev" value="%d">' % rev or '',
            'do_button': _("Do"),
            'url': self.request.href(page.page_name)
            }
        html = '''
<form class="actionsmenu" method="GET" action="%(url)s">
<div>
    <label>%(label)s</label>
    <select name="action"
        onchange="if ((this.selectedIndex != 0) &&
                      (this.options[this.selectedIndex].disabled == false)) {
                this.form.submit();
            }
            this.selectedIndex = 0;">
        %(options)s
    </select>
    <input type="submit" value="%(do_button)s">
    %(rev_field)s
</div>
<script type="text/javascript">
<!--// Init menu
actionsMenuInit('%(label)s');
//-->
</script>
</form>
''' % data

        return html

    def editbar(self, d):
        """ Assemble the page edit bar.

        Create html on first call, then return cached html.

        @param d: parameter dictionary
        @rtype: unicode
        @return: iconbar html
        """
        page = d['page']
        if not self.shouldShowEditbar(page):
            return ''

        html = self._cache.get('editbar')
        if html is None:
            # Remove empty items and format as list. The item for showing inline comments
            # is hidden by default. It gets activated through javascript only if inline
            # comments exist on the page.
            items = []
            for item in self.editbarItems(page):
                if item:
                    if 'nbcomment' in item:
                        # hiding the complete list item is cosmetically better than just
                        # hiding the contents (e.g. for sidebar themes).
                        items.append('<li class="toggleCommentsButton" style="display:none;">%s</li>' % item)
                    else:
                        items.append('<li>%s</li>' % item)
            html = u'<ul class="editbar">%s</ul>\n' % ''.join(items)
            self._cache['editbar'] = html

        return html

    def shouldShowEditbar(self, page):
        """ Should we show the editbar?

        Actions should implement this, because only the action knows if
        the edit bar makes sense. Until it goes into actions, we do the
        checking here.

        @param page: current page
        @rtype: bool
        @return: true if editbar should show
        """
        # Show editbar only for existing pages, including deleted pages,
        # that the user may read. If you may not read, you can't edit,
        # so you don't need editbar.
        if (page.exists(includeDeleted=1) and
            self.request.user.may.read(page.page_name)):
            form = self.request.form
            action = self.request.action
            # Do not show editbar on edit but on save/cancel
            return not (action == 'edit' and
                        not form.has_key('button_save') and
                        not form.has_key('button_cancel'))
        return False

    def editbarItems(self, page):
        """ Return list of items to show on the editbar

        This is separate method to make it easy to customize the
        edtibar in sub classes.
        """
        _ = self.request.getText
        editbar_actions = []
        for editbar_item in self.request.cfg.edit_bar:
            if (editbar_item == 'Discussion' and
               (self.request.getPragma('supplementation-page', self.request.cfg.supplementation_page)
                                                   in (True, 1, 'on', '1'))):
                    editbar_actions.append(self.supplementation_page_nameLink(page))
            elif editbar_item == 'Comments':
                # we just use <a> to get same style as other links, but we add some dummy
                # link target to get correct mouseover pointer appearance. return false
                # keeps the browser away from jumping to the link target::
                editbar_actions.append('<a href="#" class="nbcomment" onClick="toggleComments();return false;">%s</a>' % _('Comments'))
            elif editbar_item == 'Edit':
                editbar_actions.append(self.editorLink(page))
            elif editbar_item == 'Info':
                editbar_actions.append(self.infoLink(page))
            elif editbar_item == 'Subscribe':
                editbar_actions.append(self.subscribeLink(page))
            elif editbar_item == 'Quicklink':
                editbar_actions.append(self.quicklinkLink(page))
            elif editbar_item == 'Attachments':
                editbar_actions.append(self.attachmentsLink(page))
            elif editbar_item == 'ActionsMenu':
                editbar_actions.append(self.actionsMenu(page))
        return editbar_actions

    def supplementation_page_nameLink(self, page):
        """Return a link to the discussion page

           If the discussion page doesn't exist and the user
           has no right to create it, show a disabled link.
        """
        _ = self.request.getText
        suppl_name = self.request.cfg.supplementation_page_name
        suppl_name_full = "%s/%s" % (page.page_name, suppl_name)

        test = Page(self.request, suppl_name_full)
        if not test.exists() and not self.request.user.may.write(suppl_name_full):
            return ('<span class="disabled">%s</span>' % _(suppl_name))
        else:
            return page.link_to(self.request, text=_(suppl_name),
                                querystr={'action': 'supplementation'}, css_class='nbsupplementation', rel='nofollow')

    def guiworks(self, page):
        """ Return whether the gui editor / converter can work for that page.

            The GUI editor currently only works for wiki format.
            For simplicity, we also tell it does not work if the admin forces the text editor.
        """
        is_wiki = page.pi['format'] == 'wiki'
        gui_disallowed = self.cfg.editor_force and self.cfg.editor_default == 'text'
        return is_wiki and not gui_disallowed


    def editorLink(self, page):
        """ Return a link to the editor

        If the user can't edit, return a disabled edit link.

        If the user want to show both editors, it will display "Edit
        (Text)", otherwise as "Edit".
        """
        if 'edit' in self.request.cfg.actions_excluded:
            return ""

        if not (page.isWritable() and
                self.request.user.may.write(page.page_name)):
            return self.disabledEdit()

        _ = self.request.getText
        querystr = {'action': 'edit'}

        guiworks = self.guiworks(page)
        if self.showBothEditLinks() and guiworks:
            text = _('Edit (Text)')
            querystr['editor'] = 'text'
            attrs = {'name': 'texteditlink', 'rel': 'nofollow', }
        else:
            text = _('Edit')
            if guiworks:
                # 'textonly' will be upgraded dynamically to 'guipossible' by JS
                querystr['editor'] = 'textonly'
                attrs = {'name': 'editlink', 'rel': 'nofollow', }
            else:
                querystr['editor'] = 'text'
                attrs = {'name': 'texteditlink', 'rel': 'nofollow', }

        return page.link_to(self.request, text=text, querystr=querystr, **attrs)

    def showBothEditLinks(self):
        """ Return True if both edit links should be displayed """
        editor = self.request.user.editor_ui
        if editor == '<default>':
            editor = self.request.cfg.editor_ui
        return editor == 'freechoice'

    def guiEditorScript(self, d):
        """ Return a script that set the gui editor link variables

        The link will be created only when javascript is enabled and
        the browser is compatible with the editor.
        """
        page = d['page']
        if not (page.isWritable() and
                self.request.user.may.write(page.page_name) and
                self.showBothEditLinks() and
                self.guiworks(page)):
            return ''

        _ = self.request.getText
        return """\
<script type="text/javascript">
<!-- // GUI edit link and i18n
var gui_editor_link_href = "%(url)s";
var gui_editor_link_text = "%(text)s";
//-->
</script>
""" % {'url': page.url(self.request, querystr={'action': 'edit', 'editor': 'gui', }),
       'text': _('Edit (GUI)'),
      }

    def disabledEdit(self):
        """ Return a disabled edit link """
        _ = self.request.getText
        return ('<span class="disabled">%s</span>'
                % _('Immutable Page'))

    def infoLink(self, page):
        """ Return link to page information """
        if 'info' in self.request.cfg.actions_excluded:
            return ""

        _ = self.request.getText
        return page.link_to(self.request,
                            text=_('Info'),
                            querystr={'action': 'info'}, css_class='nbinfo', rel='nofollow')

    def subscribeLink(self, page):
        """ Return subscribe/unsubscribe link to valid users

        @rtype: unicode
        @return: subscribe or unsubscribe link
        """
        if not ((self.cfg.mail_enabled or self.cfg.jabber_enabled) and self.request.user.valid):
            return ''

        _ = self.request.getText
        if self.request.user.isSubscribedTo([page.page_name]):
            action, text = 'unsubscribe', _("Unsubscribe")
        else:
            action, text = 'subscribe', _("Subscribe")
        if action in self.request.cfg.actions_excluded:
            return ""
        return page.link_to(self.request, text=text, querystr={'action': action}, css_class='nbsubscribe', rel='nofollow')

    def quicklinkLink(self, page):
        """ Return add/remove quicklink link

        @rtype: unicode
        @return: link to add or remove a quicklink
        """
        if not self.request.user.valid:
            return ''

        _ = self.request.getText
        if self.request.user.isQuickLinkedTo([page.page_name]):
            action, text = 'quickunlink', _("Remove Link")
        else:
            action, text = 'quicklink', _("Add Link")
        if action in self.request.cfg.actions_excluded:
            return ""
        return page.link_to(self.request, text=text, querystr={'action': action}, css_class='nbquicklink', rel='nofollow')

    def attachmentsLink(self, page):
        """ Return link to page attachments """
        if 'AttachFile' in self.request.cfg.actions_excluded:
            return ""

        _ = self.request.getText
        return page.link_to(self.request,
                            text=_('Attachments'),
                            querystr={'action': 'attachf'}, css_class='nbattachments', rel='nofollow')

    def startPage(self):
        """ Start page div with page language and direction

        @rtype: unicode
        @return: page div with language and direction attribtues
        """
        return u'<div id="page"%s>\n' % self.content_lang_attr()

    def endPage(self):
        """ End page div

        Add an empty page bottom div to prevent floating elements to
        float out of the page bottom over the footer.
        """
        return '<div id="pagebottom"></div>\n</div>\n'

    # Public functions #####################################################

    def header(self, d, **kw):
        """ Assemble wiki header

        @param d: parameter dictionary
        @rtype: unicode
        @return: page header html
        """
        html = [
            # Pre header custom html
            self.emit_custom_html(self.cfg.page_header1),
            """\
<!-- BEGIN HEADER -->
<div class="page-header navbar navbar-fixed-top">
    <!-- BEGIN HEADER INNER -->
    <div class="page-header-inner">
        <!-- BEGIN LOGO -->
        <div class="page-logo">
""",
            self.logo(),
            # <a href="index.html">
            # <img src="/master/moin_static195/metronic/assets/admin/layout/img/logo.png" alt="logo" class="logo-default"/>
            # </a>
            """\
            <div class="menu-toggler sidebar-toggler hide">
            </div>
        </div>
        <!-- END LOGO -->
        <!-- BEGIN RESPONSIVE MENU TOGGLER -->
        <a href="javascript:;" class="menu-toggler responsive-toggler" data-toggle="collapse" data-target=".navbar-collapse">
        </a>
        <!-- END RESPONSIVE MENU TOGGLER -->
        <!-- BEGIN TOP NAVIGATION MENU -->
        <div class="top-menu">
            <ul class="nav navbar-nav pull-right">
                <!-- BEGIN NOTIFICATION DROPDOWN -->
                <!-- DOC: Apply "dropdown-dark" class after below "dropdown-extended" to change the dropdown styte -->
                <li class="dropdown dropdown-extended dropdown-notification" id="header_notification_bar">
                    <a href="javascript:;" class="dropdown-toggle" data-toggle="dropdown" data-hover="dropdown" data-close-others="true">
                    <i class="icon-bell"></i>
                    <span class="badge badge-default">
                    7 </span>
                    </a>
                    <ul class="dropdown-menu">
                        <li class="external">
                            <h3><span class="bold">12 pending</span> notifications</h3>
                            <a href="extra_profile.html">view all</a>
                        </li>
                        <li>
                            <ul class="dropdown-menu-list scroller" style="height: 250px;" data-handle-color="#637283">
                                <li>
                                    <a href="javascript:;">
                                    <span class="time">just now</span>
                                    <span class="details">
                                    <span class="label label-sm label-icon label-success">
                                    <i class="fa fa-plus"></i>
                                    </span>
                                    New user registered. </span>
                                    </a>
                                </li>
                                <li>
                                    <a href="javascript:;">
                                    <span class="time">3 mins</span>
                                    <span class="details">
                                    <span class="label label-sm label-icon label-danger">
                                    <i class="fa fa-bolt"></i>
                                    </span>
                                    Server #12 overloaded. </span>
                                    </a>
                                </li>
                                <li>
                                    <a href="javascript:;">
                                    <span class="time">10 mins</span>
                                    <span class="details">
                                    <span class="label label-sm label-icon label-warning">
                                    <i class="fa fa-bell-o"></i>
                                    </span>
                                    Server #2 not responding. </span>
                                    </a>
                                </li>
                                <li>
                                    <a href="javascript:;">
                                    <span class="time">14 hrs</span>
                                    <span class="details">
                                    <span class="label label-sm label-icon label-info">
                                    <i class="fa fa-bullhorn"></i>
                                    </span>
                                    Application error. </span>
                                    </a>
                                </li>
                                <li>
                                    <a href="javascript:;">
                                    <span class="time">2 days</span>
                                    <span class="details">
                                    <span class="label label-sm label-icon label-danger">
                                    <i class="fa fa-bolt"></i>
                                    </span>
                                    Database overloaded 68%. </span>
                                    </a>
                                </li>
                                <li>
                                    <a href="javascript:;">
                                    <span class="time">3 days</span>
                                    <span class="details">
                                    <span class="label label-sm label-icon label-danger">
                                    <i class="fa fa-bolt"></i>
                                    </span>
                                    A user IP blocked. </span>
                                    </a>
                                </li>
                                <li>
                                    <a href="javascript:;">
                                    <span class="time">4 days</span>
                                    <span class="details">
                                    <span class="label label-sm label-icon label-warning">
                                    <i class="fa fa-bell-o"></i>
                                    </span>
                                    Storage Server #4 not responding dfdfdfd. </span>
                                    </a>
                                </li>
                                <li>
                                    <a href="javascript:;">
                                    <span class="time">5 days</span>
                                    <span class="details">
                                    <span class="label label-sm label-icon label-info">
                                    <i class="fa fa-bullhorn"></i>
                                    </span>
                                    System Error. </span>
                                    </a>
                                </li>
                                <li>
                                    <a href="javascript:;">
                                    <span class="time">9 days</span>
                                    <span class="details">
                                    <span class="label label-sm label-icon label-danger">
                                    <i class="fa fa-bolt"></i>
                                    </span>
                                    Storage server failed. </span>
                                    </a>
                                </li>
                            </ul>
                        </li>
                    </ul>
                </li>
                <!-- END NOTIFICATION DROPDOWN -->
                <!-- BEGIN INBOX DROPDOWN -->
                <!-- DOC: Apply "dropdown-dark" class after below "dropdown-extended" to change the dropdown styte -->
                <li class="dropdown dropdown-extended dropdown-inbox" id="header_inbox_bar">
                    <a href="javascript:;" class="dropdown-toggle" data-toggle="dropdown" data-hover="dropdown" data-close-others="true">
                    <i class="icon-envelope-open"></i>
                    <span class="badge badge-default">
                    4 </span>
                    </a>
                    <ul class="dropdown-menu">
                        <li class="external">
                            <h3>You have <span class="bold">7 New</span> Messages</h3>
                            <a href="page_inbox.html">view all</a>
                        </li>
                        <li>
                            <ul class="dropdown-menu-list scroller" style="height: 275px;" data-handle-color="#637283">
                                <li>
                                    <a href="inbox.html?a=view">
                                    <span class="photo">
                                    <img src="/master/moin_static195/metronic/assets/admin/layout3/img/avatar2.jpg" class="img-circle" alt="">
                                    </span>
                                    <span class="subject">
                                    <span class="from">
                                    Lisa Wong </span>
                                    <span class="time">Just Now </span>
                                    </span>
                                    <span class="message">
                                    Vivamus sed auctor nibh congue nibh. auctor nibh auctor nibh... </span>
                                    </a>
                                </li>
                                <li>
                                    <a href="inbox.html?a=view">
                                    <span class="photo">
                                    <img src="/master/moin_static195/metronic/assets/admin/layout3/img/avatar3.jpg" class="img-circle" alt="">
                                    </span>
                                    <span class="subject">
                                    <span class="from">
                                    Richard Doe </span>
                                    <span class="time">16 mins </span>
                                    </span>
                                    <span class="message">
                                    Vivamus sed congue nibh auctor nibh congue nibh. auctor nibh auctor nibh... </span>
                                    </a>
                                </li>
                                <li>
                                    <a href="inbox.html?a=view">
                                    <span class="photo">
                                    <img src="/master/moin_static195/metronic/assets/admin/layout3/img/avatar1.jpg" class="img-circle" alt="">
                                    </span>
                                    <span class="subject">
                                    <span class="from">
                                    Bob Nilson </span>
                                    <span class="time">2 hrs </span>
                                    </span>
                                    <span class="message">
                                    Vivamus sed nibh auctor nibh congue nibh. auctor nibh auctor nibh... </span>
                                    </a>
                                </li>
                                <li>
                                    <a href="inbox.html?a=view">
                                    <span class="photo">
                                    <img src="/master/moin_static195/metronic/assets/admin/layout3/img/avatar2.jpg" class="img-circle" alt="">
                                    </span>
                                    <span class="subject">
                                    <span class="from">
                                    Lisa Wong </span>
                                    <span class="time">40 mins </span>
                                    </span>
                                    <span class="message">
                                    Vivamus sed auctor 40% nibh congue nibh... </span>
                                    </a>
                                </li>
                                <li>
                                    <a href="inbox.html?a=view">
                                    <span class="photo">
                                    <img src="/master/moin_static195/metronic/assets/admin/layout3/img/avatar3.jpg" class="img-circle" alt="">
                                    </span>
                                    <span class="subject">
                                    <span class="from">
                                    Richard Doe </span>
                                    <span class="time">46 mins </span>
                                    </span>
                                    <span class="message">
                                    Vivamus sed congue nibh auctor nibh congue nibh. auctor nibh auctor nibh... </span>
                                    </a>
                                </li>
                            </ul>
                        </li>
                    </ul>
                </li>
                <!-- END INBOX DROPDOWN -->
                <!-- BEGIN TODO DROPDOWN -->
                <!-- DOC: Apply "dropdown-dark" class after below "dropdown-extended" to change the dropdown styte -->
                <li class="dropdown dropdown-extended dropdown-tasks" id="header_task_bar">
                    <a href="javascript:;" class="dropdown-toggle" data-toggle="dropdown" data-hover="dropdown" data-close-others="true">
                    <i class="icon-calendar"></i>
                    <span class="badge badge-default">
                    3 </span>
                    </a>
                    <ul class="dropdown-menu extended tasks">
                        <li class="external">
                            <h3>You have <span class="bold">12 pending</span> tasks</h3>
                            <a href="page_todo.html">view all</a>
                        </li>
                        <li>
                            <ul class="dropdown-menu-list scroller" style="height: 275px;" data-handle-color="#637283">
                                <li>
                                    <a href="javascript:;">
                                    <span class="task">
                                    <span class="desc">New release v1.2 </span>
                                    <span class="percent">30%</span>
                                    </span>
                                    <span class="progress">
                                    <span style="width: 40%;" class="progress-bar progress-bar-success" aria-valuenow="40" aria-valuemin="0" aria-valuemax="100"><span class="sr-only">40% Complete</span></span>
                                    </span>
                                    </a>
                                </li>
                                <li>
                                    <a href="javascript:;">
                                    <span class="task">
                                    <span class="desc">Application deployment</span>
                                    <span class="percent">65%</span>
                                    </span>
                                    <span class="progress">
                                    <span style="width: 65%;" class="progress-bar progress-bar-danger" aria-valuenow="65" aria-valuemin="0" aria-valuemax="100"><span class="sr-only">65% Complete</span></span>
                                    </span>
                                    </a>
                                </li>
                                <li>
                                    <a href="javascript:;">
                                    <span class="task">
                                    <span class="desc">Mobile app release</span>
                                    <span class="percent">98%</span>
                                    </span>
                                    <span class="progress">
                                    <span style="width: 98%;" class="progress-bar progress-bar-success" aria-valuenow="98" aria-valuemin="0" aria-valuemax="100"><span class="sr-only">98% Complete</span></span>
                                    </span>
                                    </a>
                                </li>
                                <li>
                                    <a href="javascript:;">
                                    <span class="task">
                                    <span class="desc">Database migration</span>
                                    <span class="percent">10%</span>
                                    </span>
                                    <span class="progress">
                                    <span style="width: 10%;" class="progress-bar progress-bar-warning" aria-valuenow="10" aria-valuemin="0" aria-valuemax="100"><span class="sr-only">10% Complete</span></span>
                                    </span>
                                    </a>
                                </li>
                                <li>
                                    <a href="javascript:;">
                                    <span class="task">
                                    <span class="desc">Web server upgrade</span>
                                    <span class="percent">58%</span>
                                    </span>
                                    <span class="progress">
                                    <span style="width: 58%;" class="progress-bar progress-bar-info" aria-valuenow="58" aria-valuemin="0" aria-valuemax="100"><span class="sr-only">58% Complete</span></span>
                                    </span>
                                    </a>
                                </li>
                                <li>
                                    <a href="javascript:;">
                                    <span class="task">
                                    <span class="desc">Mobile development</span>
                                    <span class="percent">85%</span>
                                    </span>
                                    <span class="progress">
                                    <span style="width: 85%;" class="progress-bar progress-bar-success" aria-valuenow="85" aria-valuemin="0" aria-valuemax="100"><span class="sr-only">85% Complete</span></span>
                                    </span>
                                    </a>
                                </li>
                                <li>
                                    <a href="javascript:;">
                                    <span class="task">
                                    <span class="desc">New UI release</span>
                                    <span class="percent">38%</span>
                                    </span>
                                    <span class="progress progress-striped">
                                    <span style="width: 38%;" class="progress-bar progress-bar-important" aria-valuenow="18" aria-valuemin="0" aria-valuemax="100"><span class="sr-only">38% Complete</span></span>
                                    </span>
                                    </a>
                                </li>
                            </ul>
                        </li>
                    </ul>
                </li>
                <!-- END TODO DROPDOWN -->
                <!-- BEGIN USER LOGIN DROPDOWN -->
                <!-- DOC: Apply "dropdown-dark" class after below "dropdown-extended" to change the dropdown styte -->
                <li class="dropdown dropdown-user">
                    <a href="javascript:;" class="dropdown-toggle" data-toggle="dropdown" data-hover="dropdown" data-close-others="true">
                    <img alt="" class="img-circle" src="/master/moin_static195/metronic/assets/admin/layout/img/avatar3_small.jpg"/>
                    <span class="username username-hide-on-mobile">
                    Nick </span>
                    <i class="fa fa-angle-down"></i>
                    </a>
                    <ul class="dropdown-menu dropdown-menu-default">
                        <li>
                            <a href="extra_profile.html">
                            <i class="icon-user"></i> My Profile </a>
                        </li>
                        <li>
                            <a href="page_calendar.html">
                            <i class="icon-calendar"></i> My Calendar </a>
                        </li>
                        <li>
                            <a href="inbox.html">
                            <i class="icon-envelope-open"></i> My Inbox <span class="badge badge-danger">
                            3 </span>
                            </a>
                        </li>
                        <li>
                            <a href="page_todo.html">
                            <i class="icon-rocket"></i> My Tasks <span class="badge badge-success">
                            7 </span>
                            </a>
                        </li>
                        <li class="divider">
                        </li>
                        <li>
                            <a href="extra_lock.html">
                            <i class="icon-lock"></i> Lock Screen </a>
                        </li>
                        <li>
                            <a href="login.html">
                            <i class="icon-key"></i> Log Out </a>
                        </li>
                    </ul>
                </li>
                <!-- END USER LOGIN DROPDOWN -->
                <!-- BEGIN QUICK SIDEBAR TOGGLER -->
                <!-- DOC: Apply "dropdown-dark" class after below "dropdown-extended" to change the dropdown styte -->
                <li class="dropdown dropdown-quick-sidebar-toggler">
                    <a href="javascript:;" class="dropdown-toggle">
                    <i class="icon-logout"></i>
                    </a>
                </li>
                <!-- END QUICK SIDEBAR TOGGLER -->
            </ul>
        </div>
        <!-- END TOP NAVIGATION MENU -->
    </div>
    <!-- END HEADER INNER -->
</div>
<!-- END HEADER -->
<div class="clearfix">
</div>
<!-- BEGIN CONTAINER -->
<div class="page-container">
    <!-- BEGIN SIDEBAR -->
    <div class="page-sidebar-wrapper">
        <!-- DOC: Set data-auto-scroll="false" to disable the sidebar from auto scrolling/focusing -->
        <!-- DOC: Change data-auto-speed="200" to adjust the sub menu slide up/down speed -->
        <div class="page-sidebar navbar-collapse collapse">
            <!-- BEGIN SIDEBAR MENU -->
            <!-- DOC: Apply "page-sidebar-menu-light" class right after "page-sidebar-menu" to enable light sidebar menu style(without borders) -->
            <!-- DOC: Apply "page-sidebar-menu-hover-submenu" class right after "page-sidebar-menu" to enable hoverable(hover vs accordion) sub menu mode -->
            <!-- DOC: Apply "page-sidebar-menu-closed" class right after "page-sidebar-menu" to collapse("page-sidebar-closed" class must be applied to the body element) the sidebar sub menu mode -->
            <!-- DOC: Set data-auto-scroll="false" to disable the sidebar from auto scrolling/focusing -->
            <!-- DOC: Set data-keep-expand="true" to keep the submenues expanded -->
            <!-- DOC: Set data-auto-speed="200" to adjust the sub menu slide up/down speed -->
            <ul class="page-sidebar-menu " data-keep-expanded="false" data-auto-scroll="true" data-slide-speed="200">
                <!-- DOC: To remove the sidebar toggler from the sidebar you just need to completely remove the below "sidebar-toggler-wrapper" LI element -->
                <li class="sidebar-toggler-wrapper">
                    <!-- BEGIN SIDEBAR TOGGLER BUTTON -->
                    <div class="sidebar-toggler">
                    </div>
                    <!-- END SIDEBAR TOGGLER BUTTON -->
                </li>
                <!-- DOC: To remove the search box from the sidebar you just need to completely remove the below "sidebar-search-wrapper" LI element -->
                <li class="sidebar-search-wrapper">
                    <!-- BEGIN RESPONSIVE QUICK SEARCH FORM -->
                    <!-- DOC: Apply "sidebar-search-bordered" class the below search form to have bordered search box -->
                    <!-- DOC: Apply "sidebar-search-bordered sidebar-search-solid" class the below search form to have bordered & solid search box -->
                    <form class="sidebar-search " action="extra_search.html" method="POST">
                        <a href="javascript:;" class="remove">
                        <i class="icon-close"></i>
                        </a>
                        <div class="input-group">
                            <input type="text" class="form-control" placeholder="Search...">
                            <span class="input-group-btn">
                            <a href="javascript:;" class="btn submit"><i class="icon-magnifier"></i></a>
                            </span>
                        </div>
                    </form>
                    <!-- END RESPONSIVE QUICK SEARCH FORM -->
                </li>
                <li class="start active open">
                    <a href="javascript:;">
                    <i class="icon-home"></i>
                    <span class="title">Dashboard</span>
                    <span class="selected"></span>
                    <span class="arrow open"></span>
                    </a>
                    <ul class="sub-menu">
                        <li class="active">
                            <a href="index.html">
                            <i class="icon-bar-chart"></i>
                            Default Dashboard</a>
                        </li>
                        <li>
                            <a href="index_2.html">
                            <i class="icon-bulb"></i>
                            New Dashboard #1</a>
                        </li>
                        <li>
                            <a href="index_3.html">
                            <i class="icon-graph"></i>
                            New Dashboard #2</a>
                        </li>
                    </ul>
                </li>
                <li>
                    <a href="javascript:;">
                    <i class="icon-basket"></i>
                    <span class="title">eCommerce</span>
                    <span class="arrow "></span>
                    </a>
                    <ul class="sub-menu">
                        <li>
                            <a href="ecommerce_index.html">
                            <i class="icon-home"></i>
                            Dashboard</a>
                        </li>
                        <li>
                            <a href="ecommerce_orders.html">
                            <i class="icon-basket"></i>
                            Orders</a>
                        </li>
                        <li>
                            <a href="ecommerce_orders_view.html">
                            <i class="icon-tag"></i>
                            Order View</a>
                        </li>
                        <li>
                            <a href="ecommerce_products.html">
                            <i class="icon-handbag"></i>
                            Products</a>
                        </li>
                        <li>
                            <a href="ecommerce_products_edit.html">
                            <i class="icon-pencil"></i>
                            Product Edit</a>
                        </li>
                    </ul>
                </li>
                <li>
                    <a href="javascript:;">
                    <i class="icon-rocket"></i>
                    <span class="title">Page Layouts</span>
                    <span class="arrow "></span>
                    </a>
                    <ul class="sub-menu">
                        <li>
                            <a href="layout_horizontal_sidebar_menu.html">
                            Horizontal & Sidebar Menu</a>
                        </li>
                        <li>
                            <a href="index_horizontal_menu.html">
                            Dashboard & Mega Menu</a>
                        </li>
                        <li>
                            <a href="layout_horizontal_menu1.html">
                            Horizontal Mega Menu 1</a>
                        </li>
                        <li>
                            <a href="layout_horizontal_menu2.html">
                            Horizontal Mega Menu 2</a>
                        </li>
                        <li>
                            <a href="layout_fontawesome_icons.html">
                            <span class="badge badge-roundless badge-danger">new</span>Layout with Fontawesome Icons</a>
                        </li>
                        <li>
                            <a href="layout_glyphicons.html">
                            Layout with Glyphicon</a>
                        </li>
                        <li>
                            <a href="layout_full_height_portlet.html">
                            <span class="badge badge-roundless badge-success">new</span>Full Height Portlet</a>
                        </li>
                        <li>
                            <a href="layout_full_height_content.html">
                            <span class="badge badge-roundless badge-warning">new</span>Full Height Content</a>
                        </li>
                        <li>
                            <a href="layout_search_on_header1.html">
                            Search Box On Header 1</a>
                        </li>
                        <li>
                            <a href="layout_search_on_header2.html">
                            Search Box On Header 2</a>
                        </li>
                        <li>
                            <a href="layout_sidebar_search_option1.html">
                            Sidebar Search Option 1</a>
                        </li>
                        <li>
                            <a href="layout_sidebar_search_option2.html">
                            Sidebar Search Option 2</a>
                        </li>
                        <li>
                            <a href="layout_sidebar_reversed.html">
                            <span class="badge badge-roundless badge-warning">new</span>Right Sidebar Page</a>
                        </li>
                        <li>
                            <a href="layout_sidebar_fixed.html">
                            Sidebar Fixed Page</a>
                        </li>
                        <li>
                            <a href="layout_sidebar_closed.html">
                            Sidebar Closed Page</a>
                        </li>
                        <li>
                            <a href="layout_ajax.html">
                            Content Loading via Ajax</a>
                        </li>
                        <li>
                            <a href="layout_disabled_menu.html">
                            Disabled Menu Links</a>
                        </li>
                        <li>
                            <a href="layout_blank_page.html">
                            Blank Page</a>
                        </li>
                        <li>
                            <a href="layout_boxed_page.html">
                            Boxed Page</a>
                        </li>
                        <li>
                            <a href="layout_language_bar.html">
                            Language Switch Bar</a>
                        </li>
                    </ul>
                </li>
                <li>
                    <a href="javascript:;">
                    <i class="icon-diamond"></i>
                    <span class="title">UI Features</span>
                    <span class="arrow "></span>
                    </a>
                    <ul class="sub-menu">
                        <li>
                            <a href="ui_general.html">
                            General Components</a>
                        </li>
                        <li>
                            <a href="ui_buttons.html">
                            Buttons</a>
                        </li>
                        <li>
                            <a href="ui_confirmations.html">
                            Popover Confirmations</a>
                        </li>
                        <li>
                            <a href="ui_icons.html">
                            <span class="badge badge-roundless badge-danger">new</span>Font Icons</a>
                        </li>
                        <li>
                            <a href="ui_colors.html">
                            Flat UI Colors</a>
                        </li>
                        <li>
                            <a href="ui_typography.html">
                            Typography</a>
                        </li>
                        <li>
                            <a href="ui_tabs_accordions_navs.html">
                            Tabs, Accordions & Navs</a>
                        </li>
                        <li>
                            <a href="ui_tree.html">
                            <span class="badge badge-roundless badge-danger">new</span>Tree View</a>
                        </li>
                        <li>
                            <a href="ui_page_progress_style_1.html">
                            <span class="badge badge-roundless badge-warning">new</span>Page Progress Bar</a>
                        </li>
                        <li>
                            <a href="ui_blockui.html">
                            Block UI</a>
                        </li>
                        <li>
                            <a href="ui_bootstrap_growl.html">
                            <span class="badge badge-roundless badge-warning">new</span>Bootstrap Growl Notifications</a>
                        </li>
                        <li>
                            <a href="ui_notific8.html">
                            Notific8 Notifications</a>
                        </li>
                        <li>
                            <a href="ui_toastr.html">
                            Toastr Notifications</a>
                        </li>
                        <li>
                            <a href="ui_alert_dialog_api.html">
                            <span class="badge badge-roundless badge-danger">new</span>Alerts & Dialogs API</a>
                        </li>
                        <li>
                            <a href="ui_session_timeout.html">
                            Session Timeout</a>
                        </li>
                        <li>
                            <a href="ui_idle_timeout.html">
                            User Idle Timeout</a>
                        </li>
                        <li>
                            <a href="ui_modals.html">
                            Modals</a>
                        </li>
                        <li>
                            <a href="ui_extended_modals.html">
                            Extended Modals</a>
                        </li>
                        <li>
                            <a href="ui_tiles.html">
                            Tiles</a>
                        </li>
                        <li>
                            <a href="ui_datepaginator.html">
                            <span class="badge badge-roundless badge-success">new</span>Date Paginator</a>
                        </li>
                        <li>
                            <a href="ui_nestable.html">
                            Nestable List</a>
                        </li>
                    </ul>
                </li>
                <li>
                    <a href="javascript:;">
                    <i class="icon-puzzle"></i>
                    <span class="title">UI Components</span>
                    <span class="arrow "></span>
                    </a>
                    <ul class="sub-menu">
                        <li>
                            <a href="components_pickers.html">
                            Date & Time Pickers</a>
                        </li>
                        <li>
                            <a href="components_context_menu.html">
                            Context Menu</a>
                        </li>
                        <li>
                            <a href="components_dropdowns.html">
                            Custom Dropdowns</a>
                        </li>
                        <li>
                            <a href="components_form_tools.html">
                            Form Widgets & Tools</a>
                        </li>
                        <li>
                            <a href="components_form_tools2.html">
                            Form Widgets & Tools 2</a>
                        </li>
                        <li>
                            <a href="components_editors.html">
                            Markdown & WYSIWYG Editors</a>
                        </li>
                        <li>
                            <a href="components_ion_sliders.html">
                            Ion Range Sliders</a>
                        </li>
                        <li>
                            <a href="components_noui_sliders.html">
                            NoUI Range Sliders</a>
                        </li>
                        <li>
                            <a href="components_jqueryui_sliders.html">
                            jQuery UI Sliders</a>
                        </li>
                        <li>
                            <a href="components_knob_dials.html">
                            Knob Circle Dials</a>
                        </li>
                    </ul>
                </li>
                <!-- BEGIN ANGULARJS LINK -->
                <li class="tooltips" data-container="body" data-placement="right" data-html="true" data-original-title="AngularJS version demo">
                    <a href="angularjs" target="_blank">
                    <i class="icon-paper-plane"></i>
                    <span class="title">
                    AngularJS Version </span>
                    </a>
                </li>
                <!-- END ANGULARJS LINK -->
                <li class="heading">
                    <h3 class="uppercase">Features</h3>
                </li>
                <li>
                    <a href="javascript:;">
                    <i class="icon-settings"></i>
                    <span class="title">Form Stuff</span>
                    <span class="arrow "></span>
                    </a>
                    <ul class="sub-menu">
                        <li>
                            <a href="form_controls_md.html">
                            <span class="badge badge-roundless badge-danger">new</span>Material Design<br>
                            Form Controls</a>
                        </li>
                        <li>
                            <a href="form_controls.html">
                            Bootstrap<br>
                            Form Controls</a>
                        </li>
                        <li>
                            <a href="form_icheck.html">
                            iCheck Controls</a>
                        </li>
                        <li>
                            <a href="form_layouts.html">
                            Form Layouts</a>
                        </li>
                        <li>
                            <a href="form_editable.html">
                            <span class="badge badge-roundless badge-warning">new</span>Form X-editable</a>
                        </li>
                        <li>
                            <a href="form_wizard.html">
                            Form Wizard</a>
                        </li>
                        <li>
                            <a href="form_validation.html">
                            Form Validation</a>
                        </li>
                        <li>
                            <a href="form_image_crop.html">
                            <span class="badge badge-roundless badge-danger">new</span>Image Cropping</a>
                        </li>
                        <li>
                            <a href="form_fileupload.html">
                            Multiple File Upload</a>
                        </li>
                        <li>
                            <a href="form_dropzone.html">
                            Dropzone File Upload</a>
                        </li>
                    </ul>
                </li>
                <li>
                    <a href="javascript:;">
                    <i class="icon-briefcase"></i>
                    <span class="title">Data Tables</span>
                    <span class="arrow "></span>
                    </a>
                    <ul class="sub-menu">
                        <li>
                            <a href="table_basic.html">
                            Basic Datatables</a>
                        </li>
                        <li>
                            <a href="table_tree.html">
                            Tree Datatables</a>
                        </li>
                        <li>
                            <a href="table_responsive.html">
                            Responsive Datatables</a>
                        </li>
                        <li>
                            <a href="table_managed.html">
                            Managed Datatables</a>
                        </li>
                        <li>
                            <a href="table_editable.html">
                            Editable Datatables</a>
                        </li>
                        <li>
                            <a href="table_advanced.html">
                            Advanced Datatables</a>
                        </li>
                        <li>
                            <a href="table_ajax.html">
                            Ajax Datatables</a>
                        </li>
                    </ul>
                </li>
                <li>
                    <a href="javascript:;">
                    <i class="icon-wallet"></i>
                    <span class="title">Portlets</span>
                    <span class="arrow "></span>
                    </a>
                    <ul class="sub-menu">
                        <li>
                            <a href="portlet_general.html">
                            General Portlets</a>
                        </li>
                        <li>
                            <a href="portlet_general2.html">
                            <span class="badge badge-roundless badge-danger">new</span>New Portlets #1</a>
                        </li>
                        <li>
                            <a href="portlet_general3.html">
                            <span class="badge badge-roundless badge-danger">new</span>New Portlets #2</a>
                        </li>
                        <li>
                            <a href="portlet_ajax.html">
                            Ajax Portlets</a>
                        </li>
                        <li>
                            <a href="portlet_draggable.html">
                            Draggable Portlets</a>
                        </li>
                    </ul>
                </li>
                <li>
                    <a href="javascript:;">
                    <i class="icon-bar-chart"></i>
                    <span class="title">Charts</span>
                    <span class="arrow "></span>
                    </a>
                    <ul class="sub-menu">
                        <li>
                            <a href="charts_amcharts.html">
                            amChart</a>
                        </li>
                        <li>
                            <a href="charts_flotcharts.html">
                            Flotchart</a>
                        </li>
                    </ul>
                </li>
                <li>
                    <a href="javascript:;">
                    <i class="icon-docs"></i>
                    <span class="title">Pages</span>
                    <span class="arrow "></span>
                    </a>
                    <ul class="sub-menu">
                        <li>
                            <a href="page_timeline.html">
                            <i class="icon-paper-plane"></i>
                            <span class="badge badge-warning">2</span>New Timeline</a>
                        </li>
                        <li>
                            <a href="extra_profile.html">
                            <i class="icon-user-following"></i>
                            <span class="badge badge-success badge-roundless">new</span>New User Profile</a>
                        </li>
                        <li>
                            <a href="page_todo.html">
                            <i class="icon-check"></i>
                            Todo</a>
                        </li>
                        <li>
                            <a href="inbox.html">
                            <i class="icon-envelope"></i>
                            <span class="badge badge-danger">4</span>Inbox</a>
                        </li>
                        <li>
                            <a href="extra_faq.html">
                            <i class="icon-question"></i>
                            FAQ</a>
                        </li>
                        <li>
                            <a href="page_calendar.html">
                            <i class="icon-calendar"></i>
                            <span class="badge badge-danger">14</span>Calendar</a>
                        </li>
                        <li>
                            <a href="page_coming_soon.html">
                            <i class="icon-flag"></i>
                            Coming Soon</a>
                        </li>
                        <li>
                            <a href="page_blog.html">
                            <i class="icon-speech"></i>
                            Blog</a>
                        </li>
                        <li>
                            <a href="page_blog_item.html">
                            <i class="icon-link"></i>
                            Blog Post</a>
                        </li>
                        <li>
                            <a href="page_news.html">
                            <i class="icon-eye"></i>
                            <span class="badge badge-success">9</span>News</a>
                        </li>
                        <li>
                            <a href="page_news_item.html">
                            <i class="icon-bell"></i>
                            News View</a>
                        </li>
                        <li>
                            <a href="page_timeline_old.html">
                            <i class="icon-paper-plane"></i>
                            <span class="badge badge-warning">2</span>Old Timeline</a>
                        </li>
                        <li>
                            <a href="extra_profile_old.html">
                            <i class="icon-user"></i>
                            Old User Profile</a>
                        </li>
                    </ul>
                </li>
                <li>
                    <a href="javascript:;">
                    <i class="icon-present"></i>
                    <span class="title">Extra</span>
                    <span class="arrow "></span>
                    </a>
                    <ul class="sub-menu">
                        <li>
                            <a href="page_about.html">
                            About Us</a>
                        </li>
                        <li>
                            <a href="page_contact.html">
                            Contact Us</a>
                        </li>
                        <li>
                            <a href="extra_search.html">
                            Search Results</a>
                        </li>
                        <li>
                            <a href="extra_invoice.html">
                            Invoice</a>
                        </li>
                        <li>
                            <a href="page_portfolio.html">
                            Portfolio</a>
                        </li>
                        <li>
                            <a href="extra_pricing_table.html">
                            Pricing Tables</a>
                        </li>
                        <li>
                            <a href="extra_404_option1.html">
                            404 Page Option 1</a>
                        </li>
                        <li>
                            <a href="extra_404_option2.html">
                            404 Page Option 2</a>
                        </li>
                        <li>
                            <a href="extra_404_option3.html">
                            404 Page Option 3</a>
                        </li>
                        <li>
                            <a href="extra_500_option1.html">
                            500 Page Option 1</a>
                        </li>
                        <li>
                            <a href="extra_500_option2.html">
                            500 Page Option 2</a>
                        </li>
                    </ul>
                </li>
                <li>
                    <a href="javascript:;">
                    <i class="icon-folder"></i>
                    <span class="title">Multi Level Menu</span>
                    <span class="arrow "></span>
                    </a>
                    <ul class="sub-menu">
                        <li>
                            <a href="javascript:;">
                            <i class="icon-settings"></i> Item 1 <span class="arrow"></span>
                            </a>
                            <ul class="sub-menu">
                                <li>
                                    <a href="javascript:;">
                                    <i class="icon-user"></i>
                                    Sample Link 1 <span class="arrow"></span>
                                    </a>
                                    <ul class="sub-menu">
                                        <li>
                                            <a href="#"><i class="icon-power"></i> Sample Link 1</a>
                                        </li>
                                        <li>
                                            <a href="#"><i class="icon-paper-plane"></i> Sample Link 1</a>
                                        </li>
                                        <li>
                                            <a href="#"><i class="icon-star"></i> Sample Link 1</a>
                                        </li>
                                    </ul>
                                </li>
                                <li>
                                    <a href="#"><i class="icon-camera"></i> Sample Link 1</a>
                                </li>
                                <li>
                                    <a href="#"><i class="icon-link"></i> Sample Link 2</a>
                                </li>
                                <li>
                                    <a href="#"><i class="icon-pointer"></i> Sample Link 3</a>
                                </li>
                            </ul>
                        </li>
                        <li>
                            <a href="javascript:;">
                            <i class="icon-globe"></i> Item 2 <span class="arrow"></span>
                            </a>
                            <ul class="sub-menu">
                                <li>
                                    <a href="#"><i class="icon-tag"></i> Sample Link 1</a>
                                </li>
                                <li>
                                    <a href="#"><i class="icon-pencil"></i> Sample Link 1</a>
                                </li>
                                <li>
                                    <a href="#"><i class="icon-graph"></i> Sample Link 1</a>
                                </li>
                            </ul>
                        </li>
                        <li>
                            <a href="#">
                            <i class="icon-bar-chart"></i>
                            Item 3 </a>
                        </li>
                    </ul>
                </li>
                <li>
                    <a href="javascript:;">
                    <i class="icon-user"></i>
                    <span class="title">Login Options</span>
                    <span class="arrow "></span>
                    </a>
                    <ul class="sub-menu">
                        <li>
                            <a href="login.html">
                            Login Form 1</a>
                        </li>
                        <li>
                            <a href="login_2.html">
                            Login Form 2</a>
                        </li>
                        <li>
                            <a href="login_3.html">
                            Login Form 3</a>
                        </li>
                        <li>
                            <a href="login_soft.html">
                            Login Form 4</a>
                        </li>
                        <li>
                            <a href="extra_lock.html">
                            Lock Screen 1</a>
                        </li>
                        <li>
                            <a href="extra_lock2.html">
                            Lock Screen 2</a>
                        </li>
                    </ul>
                </li>
                <li class="heading">
                    <h3 class="uppercase">More</h3>
                </li>
                <li>
                    <a href="javascript:;">
                    <i class="icon-logout"></i>
                    <span class="title">Quick Sidebar</span>
                    <span class="arrow "></span>
                    </a>
                    <ul class="sub-menu">
                        <li>
                            <a href="quick_sidebar_push_content.html">
                            Push Content</a>
                        </li>
                        <li>
                            <a href="quick_sidebar_over_content.html">
                            Over Content</a>
                        </li>
                        <li>
                            <a href="quick_sidebar_over_content_transparent.html">
                            Over Content & Transparent</a>
                        </li>
                        <li>
                            <a href="quick_sidebar_on_boxed_layout.html">
                            Boxed Layout</a>
                        </li>
                    </ul>
                </li>

                <li class="last ">
                    <a href="javascript:;">
                    <i class="icon-pointer"></i>
                    <span class="title">Maps</span>
                    <span class="arrow "></span>
                    </a>
                    <ul class="sub-menu">
                        <li>
                            <a href="maps_google.html">
                            Google Maps</a>
                        </li>
                        <li>
                            <a href="maps_vector.html">
                            Vector Maps</a>
                        </li>
                    </ul>
                </li>
            </ul>
            <!-- END SIDEBAR MENU -->
        </div>
    </div>
    <!-- END SIDEBAR -->
    <!-- BEGIN CONTENT -->
    <div class="page-content-wrapper">
        <div class="page-content">
            <!-- BEGIN SAMPLE PORTLET CONFIGURATION MODAL FORM-->
            <div class="modal fade" id="portlet-config" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <button type="button" class="close" data-dismiss="modal" aria-hidden="true"></button>
                            <h4 class="modal-title">Modal title</h4>
                        </div>
                        <div class="modal-body">
                             Widget settings form goes here
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn blue">Save changes</button>
                            <button type="button" class="btn default" data-dismiss="modal">Close</button>
                        </div>
                    </div>
                    <!-- /.modal-content -->
                </div>
                <!-- /.modal-dialog -->
            </div>
            <!-- /.modal -->
            <!-- END SAMPLE PORTLET CONFIGURATION MODAL FORM-->
            <!-- BEGIN STYLE CUSTOMIZER -->
            <div class="theme-panel hidden-xs hidden-sm">
                <div class="toggler">
                </div>
                <div class="toggler-close">
                </div>
                <div class="theme-options">
                    <div class="theme-option theme-colors clearfix">
                        <span>
                        THEME COLOR </span>
                        <ul>
                            <li class="color-default current tooltips" data-style="default" data-container="body" data-original-title="Default">
                            </li>
                            <li class="color-darkblue tooltips" data-style="darkblue" data-container="body" data-original-title="Dark Blue">
                            </li>
                            <li class="color-blue tooltips" data-style="blue" data-container="body" data-original-title="Blue">
                            </li>
                            <li class="color-grey tooltips" data-style="grey" data-container="body" data-original-title="Grey">
                            </li>
                            <li class="color-light tooltips" data-style="light" data-container="body" data-original-title="Light">
                            </li>
                            <li class="color-light2 tooltips" data-style="light2" data-container="body" data-html="true" data-original-title="Light 2">
                            </li>
                        </ul>
                    </div>
                    <div class="theme-option">
                        <span>
                        Theme Style </span>
                        <select class="layout-style-option form-control input-sm">
                            <option value="square" selected="selected">Square corners</option>
                            <option value="rounded">Rounded corners</option>
                        </select>
                    </div>
                    <div class="theme-option">
                        <span>
                        Layout </span>
                        <select class="layout-option form-control input-sm">
                            <option value="fluid" selected="selected">Fluid</option>
                            <option value="boxed">Boxed</option>
                        </select>
                    </div>
                    <div class="theme-option">
                        <span>
                        Header </span>
                        <select class="page-header-option form-control input-sm">
                            <option value="fixed" selected="selected">Fixed</option>
                            <option value="default">Default</option>
                        </select>
                    </div>
                    <div class="theme-option">
                        <span>
                        Top Menu Dropdown</span>
                        <select class="page-header-top-dropdown-style-option form-control input-sm">
                            <option value="light" selected="selected">Light</option>
                            <option value="dark">Dark</option>
                        </select>
                    </div>
                    <div class="theme-option">
                        <span>
                        Sidebar Mode</span>
                        <select class="sidebar-option form-control input-sm">
                            <option value="fixed">Fixed</option>
                            <option value="default" selected="selected">Default</option>
                        </select>
                    </div>
                    <div class="theme-option">
                        <span>
                        Sidebar Menu </span>
                        <select class="sidebar-menu-option form-control input-sm">
                            <option value="accordion" selected="selected">Accordion</option>
                            <option value="hover">Hover</option>
                        </select>
                    </div>
                    <div class="theme-option">
                        <span>
                        Sidebar Style </span>
                        <select class="sidebar-style-option form-control input-sm">
                            <option value="default" selected="selected">Default</option>
                            <option value="light">Light</option>
                        </select>
                    </div>
                    <div class="theme-option">
                        <span>
                        Sidebar Position </span>
                        <select class="sidebar-pos-option form-control input-sm">
                            <option value="left" selected="selected">Left</option>
                            <option value="right">Right</option>
                        </select>
                    </div>
                    <div class="theme-option">
                        <span>
                        Footer </span>
                        <select class="page-footer-option form-control input-sm">
                            <option value="fixed">Fixed</option>
                            <option value="default" selected="selected">Default</option>
                        </select>
                    </div>
                </div>
            </div>
            <!-- END STYLE CUSTOMIZER -->
            <!-- BEGIN PAGE HEADER-->
            <div class="page-bar">
                <ul class="page-breadcrumb">
                    <li>
                        <i class="fa fa-home"></i>
                        <a href="index.html">Home</a>
                        <i class="fa fa-angle-right"></i>
                    </li>
                    <li>
                        <a href="#">Dashboard</a>
                    </li>
                </ul>
                <div class="page-toolbar">
                    <div id="dashboard-report-range" class="pull-right tooltips btn btn-sm btn-default" data-container="body" data-placement="bottom" data-original-title="Change dashboard date range">
                        <i class="icon-calendar"></i>&nbsp; <span class="thin uppercase visible-lg-inline-block"></span>&nbsp; <i class="fa fa-angle-down"></i>
                    </div>
                </div>
            </div>
""",
            """<h3 class="page-title">""",
            # Dashboard <small>reports & statistics</small>
            self.title_with_separators(d),
            """</h3>
            <!-- END PAGE HEADER-->
""", 
            # u'<div id="header">',
            # # self.searchform(d),
            # # self.logo(),
            # self.username(d),
            # u'<h1 id="locationline">',
            # self.interwiki(d),
            # self.title_with_separators(d),
            # u'</h1>',
            # self.trail(d),
            # self.navibar(d),
            # #u'<hr id="pageline">',
            # u'<div id="pageline"><hr style="display:none;"></div>',
            # self.msg(d),
            # self.editbar(d),
            # u'</div>',

            # Post header custom html (not recommended)
            self.emit_custom_html(self.cfg.page_header2),

            # Start of page
            self.startPage(),
        ]
        return u'\n'.join(html)

    editorheader = header

    def footer(self, d, **keywords):
        """ Assemble wiki footer

        @param d: parameter dictionary
        @keyword ...:...
        @rtype: unicode
        @return: page footer html
        """
        page = d['page']
        html = [
            # # End of page
            # self.pageinfo(page),
            self.endPage(),


            # Pre footer custom html (not recommended!)
            self.emit_custom_html(self.cfg.page_footer1),

            """\
        </div>
    </div>
    <!-- END CONTENT -->
    <!-- BEGIN QUICK SIDEBAR -->
    <a href="javascript:;" class="page-quick-sidebar-toggler"><i class="icon-close"></i></a>
    <div class="page-quick-sidebar-wrapper">
        <div class="page-quick-sidebar">
            <div class="nav-justified">
                <ul class="nav nav-tabs nav-justified">
                    <li class="active">
                        <a href="#quick_sidebar_tab_1" data-toggle="tab">
                        Users <span class="badge badge-danger">2</span>
                        </a>
                    </li>
                    <li>
                        <a href="#quick_sidebar_tab_2" data-toggle="tab">
                        Alerts <span class="badge badge-success">7</span>
                        </a>
                    </li>
                    <li class="dropdown">
                        <a href="javascript:;" class="dropdown-toggle" data-toggle="dropdown">
                        More<i class="fa fa-angle-down"></i>
                        </a>
                        <ul class="dropdown-menu pull-right" role="menu">
                            <li>
                                <a href="#quick_sidebar_tab_3" data-toggle="tab">
                                <i class="icon-bell"></i> Alerts </a>
                            </li>
                            <li>
                                <a href="#quick_sidebar_tab_3" data-toggle="tab">
                                <i class="icon-info"></i> Notifications </a>
                            </li>
                            <li>
                                <a href="#quick_sidebar_tab_3" data-toggle="tab">
                                <i class="icon-speech"></i> Activities </a>
                            </li>
                            <li class="divider">
                            </li>
                            <li>
                                <a href="#quick_sidebar_tab_3" data-toggle="tab">
                                <i class="icon-settings"></i> Settings </a>
                            </li>
                        </ul>
                    </li>
                </ul>
                <div class="tab-content">
                    <div class="tab-pane active page-quick-sidebar-chat" id="quick_sidebar_tab_1">
                        <div class="page-quick-sidebar-chat-users" data-rail-color="#ddd" data-wrapper-class="page-quick-sidebar-list">
                            <h3 class="list-heading">Staff</h3>
                            <ul class="media-list list-items">
                                <li class="media">
                                    <div class="media-status">
                                        <span class="badge badge-success">8</span>
                                    </div>
                                    <img class="media-object" src="/master/moin_static195/metronic/assets/admin/layout/img/avatar3.jpg" alt="...">
                                    <div class="media-body">
                                        <h4 class="media-heading">Bob Nilson</h4>
                                        <div class="media-heading-sub">
                                             Project Manager
                                        </div>
                                    </div>
                                </li>
                                <li class="media">
                                    <img class="media-object" src="/master/moin_static195/metronic/assets/admin/layout/img/avatar1.jpg" alt="...">
                                    <div class="media-body">
                                        <h4 class="media-heading">Nick Larson</h4>
                                        <div class="media-heading-sub">
                                             Art Director
                                        </div>
                                    </div>
                                </li>
                                <li class="media">
                                    <div class="media-status">
                                        <span class="badge badge-danger">3</span>
                                    </div>
                                    <img class="media-object" src="/master/moin_static195/metronic/assets/admin/layout/img/avatar4.jpg" alt="...">
                                    <div class="media-body">
                                        <h4 class="media-heading">Deon Hubert</h4>
                                        <div class="media-heading-sub">
                                             CTO
                                        </div>
                                    </div>
                                </li>
                                <li class="media">
                                    <img class="media-object" src="/master/moin_static195/metronic/assets/admin/layout/img/avatar2.jpg" alt="...">
                                    <div class="media-body">
                                        <h4 class="media-heading">Ella Wong</h4>
                                        <div class="media-heading-sub">
                                             CEO
                                        </div>
                                    </div>
                                </li>
                            </ul>
                            <h3 class="list-heading">Customers</h3>
                            <ul class="media-list list-items">
                                <li class="media">
                                    <div class="media-status">
                                        <span class="badge badge-warning">2</span>
                                    </div>
                                    <img class="media-object" src="/master/moin_static195/metronic/assets/admin/layout/img/avatar6.jpg" alt="...">
                                    <div class="media-body">
                                        <h4 class="media-heading">Lara Kunis</h4>
                                        <div class="media-heading-sub">
                                             CEO, Loop Inc
                                        </div>
                                        <div class="media-heading-small">
                                             Last seen 03:10 AM
                                        </div>
                                    </div>
                                </li>
                                <li class="media">
                                    <div class="media-status">
                                        <span class="label label-sm label-success">new</span>
                                    </div>
                                    <img class="media-object" src="/master/moin_static195/metronic/assets/admin/layout/img/avatar7.jpg" alt="...">
                                    <div class="media-body">
                                        <h4 class="media-heading">Ernie Kyllonen</h4>
                                        <div class="media-heading-sub">
                                             Project Manager,<br>
                                             SmartBizz PTL
                                        </div>
                                    </div>
                                </li>
                                <li class="media">
                                    <img class="media-object" src="/master/moin_static195/metronic/assets/admin/layout/img/avatar8.jpg" alt="...">
                                    <div class="media-body">
                                        <h4 class="media-heading">Lisa Stone</h4>
                                        <div class="media-heading-sub">
                                             CTO, Keort Inc
                                        </div>
                                        <div class="media-heading-small">
                                             Last seen 13:10 PM
                                        </div>
                                    </div>
                                </li>
                                <li class="media">
                                    <div class="media-status">
                                        <span class="badge badge-success">7</span>
                                    </div>
                                    <img class="media-object" src="/master/moin_static195/metronic/assets/admin/layout/img/avatar9.jpg" alt="...">
                                    <div class="media-body">
                                        <h4 class="media-heading">Deon Portalatin</h4>
                                        <div class="media-heading-sub">
                                             CFO, H&D LTD
                                        </div>
                                    </div>
                                </li>
                                <li class="media">
                                    <img class="media-object" src="/master/moin_static195/metronic/assets/admin/layout/img/avatar10.jpg" alt="...">
                                    <div class="media-body">
                                        <h4 class="media-heading">Irina Savikova</h4>
                                        <div class="media-heading-sub">
                                             CEO, Tizda Motors Inc
                                        </div>
                                    </div>
                                </li>
                                <li class="media">
                                    <div class="media-status">
                                        <span class="badge badge-danger">4</span>
                                    </div>
                                    <img class="media-object" src="/master/moin_static195/metronic/assets/admin/layout/img/avatar11.jpg" alt="...">
                                    <div class="media-body">
                                        <h4 class="media-heading">Maria Gomez</h4>
                                        <div class="media-heading-sub">
                                             Manager, Infomatic Inc
                                        </div>
                                        <div class="media-heading-small">
                                             Last seen 03:10 AM
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </div>
                        <div class="page-quick-sidebar-item">
                            <div class="page-quick-sidebar-chat-user">
                                <div class="page-quick-sidebar-nav">
                                    <a href="javascript:;" class="page-quick-sidebar-back-to-list"><i class="icon-arrow-left"></i>Back</a>
                                </div>
                                <div class="page-quick-sidebar-chat-user-messages">
                                    <div class="post out">
                                        <img class="avatar" alt="" src="/master/moin_static195/metronic/assets/admin/layout/img/avatar3.jpg"/>
                                        <div class="message">
                                            <span class="arrow"></span>
                                            <a href="javascript:;" class="name">Bob Nilson</a>
                                            <span class="datetime">20:15</span>
                                            <span class="body">
                                            When could you send me the report ? </span>
                                        </div>
                                    </div>
                                    <div class="post in">
                                        <img class="avatar" alt="" src="/master/moin_static195/metronic/assets/admin/layout/img/avatar2.jpg"/>
                                        <div class="message">
                                            <span class="arrow"></span>
                                            <a href="javascript:;" class="name">Ella Wong</a>
                                            <span class="datetime">20:15</span>
                                            <span class="body">
                                            Its almost done. I will be sending it shortly </span>
                                        </div>
                                    </div>
                                    <div class="post out">
                                        <img class="avatar" alt="" src="/master/moin_static195/metronic/assets/admin/layout/img/avatar3.jpg"/>
                                        <div class="message">
                                            <span class="arrow"></span>
                                            <a href="javascript:;" class="name">Bob Nilson</a>
                                            <span class="datetime">20:15</span>
                                            <span class="body">
                                            Alright. Thanks! :) </span>
                                        </div>
                                    </div>
                                    <div class="post in">
                                        <img class="avatar" alt="" src="/master/moin_static195/metronic/assets/admin/layout/img/avatar2.jpg"/>
                                        <div class="message">
                                            <span class="arrow"></span>
                                            <a href="javascript:;" class="name">Ella Wong</a>
                                            <span class="datetime">20:16</span>
                                            <span class="body">
                                            You are most welcome. Sorry for the delay. </span>
                                        </div>
                                    </div>
                                    <div class="post out">
                                        <img class="avatar" alt="" src="/master/moin_static195/metronic/assets/admin/layout/img/avatar3.jpg"/>
                                        <div class="message">
                                            <span class="arrow"></span>
                                            <a href="javascript:;" class="name">Bob Nilson</a>
                                            <span class="datetime">20:17</span>
                                            <span class="body">
                                            No probs. Just take your time :) </span>
                                        </div>
                                    </div>
                                    <div class="post in">
                                        <img class="avatar" alt="" src="/master/moin_static195/metronic/assets/admin/layout/img/avatar2.jpg"/>
                                        <div class="message">
                                            <span class="arrow"></span>
                                            <a href="javascript:;" class="name">Ella Wong</a>
                                            <span class="datetime">20:40</span>
                                            <span class="body">
                                            Alright. I just emailed it to you. </span>
                                        </div>
                                    </div>
                                    <div class="post out">
                                        <img class="avatar" alt="" src="/master/moin_static195/metronic/assets/admin/layout/img/avatar3.jpg"/>
                                        <div class="message">
                                            <span class="arrow"></span>
                                            <a href="javascript:;" class="name">Bob Nilson</a>
                                            <span class="datetime">20:17</span>
                                            <span class="body">
                                            Great! Thanks. Will check it right away. </span>
                                        </div>
                                    </div>
                                    <div class="post in">
                                        <img class="avatar" alt="" src="/master/moin_static195/metronic/assets/admin/layout/img/avatar2.jpg"/>
                                        <div class="message">
                                            <span class="arrow"></span>
                                            <a href="javascript:;" class="name">Ella Wong</a>
                                            <span class="datetime">20:40</span>
                                            <span class="body">
                                            Please let me know if you have any comment. </span>
                                        </div>
                                    </div>
                                    <div class="post out">
                                        <img class="avatar" alt="" src="/master/moin_static195/metronic/assets/admin/layout/img/avatar3.jpg"/>
                                        <div class="message">
                                            <span class="arrow"></span>
                                            <a href="javascript:;" class="name">Bob Nilson</a>
                                            <span class="datetime">20:17</span>
                                            <span class="body">
                                            Sure. I will check and buzz you if anything needs to be corrected. </span>
                                        </div>
                                    </div>
                                </div>
                                <div class="page-quick-sidebar-chat-user-form">
                                    <div class="input-group">
                                        <input type="text" class="form-control" placeholder="Type a message here...">
                                        <div class="input-group-btn">
                                            <button type="button" class="btn blue"><i class="icon-paper-clip"></i></button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="tab-pane page-quick-sidebar-alerts" id="quick_sidebar_tab_2">
                        <div class="page-quick-sidebar-alerts-list">
                            <h3 class="list-heading">General</h3>
                            <ul class="feeds list-items">
                                <li>
                                    <div class="col1">
                                        <div class="cont">
                                            <div class="cont-col1">
                                                <div class="label label-sm label-info">
                                                    <i class="fa fa-check"></i>
                                                </div>
                                            </div>
                                            <div class="cont-col2">
                                                <div class="desc">
                                                     You have 4 pending tasks. <span class="label label-sm label-warning ">
                                                    Take action <i class="fa fa-share"></i>
                                                    </span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col2">
                                        <div class="date">
                                             Just now
                                        </div>
                                    </div>
                                </li>
                                <li>
                                    <a href="javascript:;">
                                    <div class="col1">
                                        <div class="cont">
                                            <div class="cont-col1">
                                                <div class="label label-sm label-success">
                                                    <i class="fa fa-bar-chart-o"></i>
                                                </div>
                                            </div>
                                            <div class="cont-col2">
                                                <div class="desc">
                                                     Finance Report for year 2013 has been released.
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col2">
                                        <div class="date">
                                             20 mins
                                        </div>
                                    </div>
                                    </a>
                                </li>
                                <li>
                                    <div class="col1">
                                        <div class="cont">
                                            <div class="cont-col1">
                                                <div class="label label-sm label-danger">
                                                    <i class="fa fa-user"></i>
                                                </div>
                                            </div>
                                            <div class="cont-col2">
                                                <div class="desc">
                                                     You have 5 pending membership that requires a quick review.
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col2">
                                        <div class="date">
                                             24 mins
                                        </div>
                                    </div>
                                </li>
                                <li>
                                    <div class="col1">
                                        <div class="cont">
                                            <div class="cont-col1">
                                                <div class="label label-sm label-info">
                                                    <i class="fa fa-shopping-cart"></i>
                                                </div>
                                            </div>
                                            <div class="cont-col2">
                                                <div class="desc">
                                                     New order received with <span class="label label-sm label-success">
                                                    Reference Number: DR23923 </span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col2">
                                        <div class="date">
                                             30 mins
                                        </div>
                                    </div>
                                </li>
                                <li>
                                    <div class="col1">
                                        <div class="cont">
                                            <div class="cont-col1">
                                                <div class="label label-sm label-success">
                                                    <i class="fa fa-user"></i>
                                                </div>
                                            </div>
                                            <div class="cont-col2">
                                                <div class="desc">
                                                     You have 5 pending membership that requires a quick review.
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col2">
                                        <div class="date">
                                             24 mins
                                        </div>
                                    </div>
                                </li>
                                <li>
                                    <div class="col1">
                                        <div class="cont">
                                            <div class="cont-col1">
                                                <div class="label label-sm label-info">
                                                    <i class="fa fa-bell-o"></i>
                                                </div>
                                            </div>
                                            <div class="cont-col2">
                                                <div class="desc">
                                                     Web server hardware needs to be upgraded. <span class="label label-sm label-warning">
                                                    Overdue </span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col2">
                                        <div class="date">
                                             2 hours
                                        </div>
                                    </div>
                                </li>
                                <li>
                                    <a href="javascript:;">
                                    <div class="col1">
                                        <div class="cont">
                                            <div class="cont-col1">
                                                <div class="label label-sm label-default">
                                                    <i class="fa fa-briefcase"></i>
                                                </div>
                                            </div>
                                            <div class="cont-col2">
                                                <div class="desc">
                                                     IPO Report for year 2013 has been released.
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col2">
                                        <div class="date">
                                             20 mins
                                        </div>
                                    </div>
                                    </a>
                                </li>
                            </ul>
                            <h3 class="list-heading">System</h3>
                            <ul class="feeds list-items">
                                <li>
                                    <div class="col1">
                                        <div class="cont">
                                            <div class="cont-col1">
                                                <div class="label label-sm label-info">
                                                    <i class="fa fa-check"></i>
                                                </div>
                                            </div>
                                            <div class="cont-col2">
                                                <div class="desc">
                                                     You have 4 pending tasks. <span class="label label-sm label-warning ">
                                                    Take action <i class="fa fa-share"></i>
                                                    </span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col2">
                                        <div class="date">
                                             Just now
                                        </div>
                                    </div>
                                </li>
                                <li>
                                    <a href="javascript:;">
                                    <div class="col1">
                                        <div class="cont">
                                            <div class="cont-col1">
                                                <div class="label label-sm label-danger">
                                                    <i class="fa fa-bar-chart-o"></i>
                                                </div>
                                            </div>
                                            <div class="cont-col2">
                                                <div class="desc">
                                                     Finance Report for year 2013 has been released.
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col2">
                                        <div class="date">
                                             20 mins
                                        </div>
                                    </div>
                                    </a>
                                </li>
                                <li>
                                    <div class="col1">
                                        <div class="cont">
                                            <div class="cont-col1">
                                                <div class="label label-sm label-default">
                                                    <i class="fa fa-user"></i>
                                                </div>
                                            </div>
                                            <div class="cont-col2">
                                                <div class="desc">
                                                     You have 5 pending membership that requires a quick review.
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col2">
                                        <div class="date">
                                             24 mins
                                        </div>
                                    </div>
                                </li>
                                <li>
                                    <div class="col1">
                                        <div class="cont">
                                            <div class="cont-col1">
                                                <div class="label label-sm label-info">
                                                    <i class="fa fa-shopping-cart"></i>
                                                </div>
                                            </div>
                                            <div class="cont-col2">
                                                <div class="desc">
                                                     New order received with <span class="label label-sm label-success">
                                                    Reference Number: DR23923 </span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col2">
                                        <div class="date">
                                             30 mins
                                        </div>
                                    </div>
                                </li>
                                <li>
                                    <div class="col1">
                                        <div class="cont">
                                            <div class="cont-col1">
                                                <div class="label label-sm label-success">
                                                    <i class="fa fa-user"></i>
                                                </div>
                                            </div>
                                            <div class="cont-col2">
                                                <div class="desc">
                                                     You have 5 pending membership that requires a quick review.
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col2">
                                        <div class="date">
                                             24 mins
                                        </div>
                                    </div>
                                </li>
                                <li>
                                    <div class="col1">
                                        <div class="cont">
                                            <div class="cont-col1">
                                                <div class="label label-sm label-warning">
                                                    <i class="fa fa-bell-o"></i>
                                                </div>
                                            </div>
                                            <div class="cont-col2">
                                                <div class="desc">
                                                     Web server hardware needs to be upgraded. <span class="label label-sm label-default ">
                                                    Overdue </span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col2">
                                        <div class="date">
                                             2 hours
                                        </div>
                                    </div>
                                </li>
                                <li>
                                    <a href="javascript:;">
                                    <div class="col1">
                                        <div class="cont">
                                            <div class="cont-col1">
                                                <div class="label label-sm label-info">
                                                    <i class="fa fa-briefcase"></i>
                                                </div>
                                            </div>
                                            <div class="cont-col2">
                                                <div class="desc">
                                                     IPO Report for year 2013 has been released.
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col2">
                                        <div class="date">
                                             20 mins
                                        </div>
                                    </div>
                                    </a>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div class="tab-pane page-quick-sidebar-settings" id="quick_sidebar_tab_3">
                        <div class="page-quick-sidebar-settings-list">
                            <h3 class="list-heading">General Settings</h3>
                            <ul class="list-items borderless">
                                <li>
                                     Enable Notifications <input type="checkbox" class="make-switch" checked data-size="small" data-on-color="success" data-on-text="ON" data-off-color="default" data-off-text="OFF">
                                </li>
                                <li>
                                     Allow Tracking <input type="checkbox" class="make-switch" data-size="small" data-on-color="info" data-on-text="ON" data-off-color="default" data-off-text="OFF">
                                </li>
                                <li>
                                     Log Errors <input type="checkbox" class="make-switch" checked data-size="small" data-on-color="danger" data-on-text="ON" data-off-color="default" data-off-text="OFF">
                                </li>
                                <li>
                                     Auto Sumbit Issues <input type="checkbox" class="make-switch" data-size="small" data-on-color="warning" data-on-text="ON" data-off-color="default" data-off-text="OFF">
                                </li>
                                <li>
                                     Enable SMS Alerts <input type="checkbox" class="make-switch" checked data-size="small" data-on-color="success" data-on-text="ON" data-off-color="default" data-off-text="OFF">
                                </li>
                            </ul>
                            <h3 class="list-heading">System Settings</h3>
                            <ul class="list-items borderless">
                                <li>
                                     Security Level
                                    <select class="form-control input-inline input-sm input-small">
                                        <option value="1">Normal</option>
                                        <option value="2" selected>Medium</option>
                                        <option value="e">High</option>
                                    </select>
                                </li>
                                <li>
                                     Failed Email Attempts <input class="form-control input-inline input-sm input-small" value="5"/>
                                </li>
                                <li>
                                     Secondary SMTP Port <input class="form-control input-inline input-sm input-small" value="3560"/>
                                </li>
                                <li>
                                     Notify On System Error <input type="checkbox" class="make-switch" checked data-size="small" data-on-color="danger" data-on-text="ON" data-off-color="default" data-off-text="OFF">
                                </li>
                                <li>
                                     Notify On SMTP Error <input type="checkbox" class="make-switch" checked data-size="small" data-on-color="warning" data-on-text="ON" data-off-color="default" data-off-text="OFF">
                                </li>
                            </ul>
                            <div class="inner-content">
                                <button class="btn btn-success"><i class="icon-settings"></i> Save Changes</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- END QUICK SIDEBAR -->
</div>
<!-- END CONTAINER -->
""",
            # # Footer
            # u'<div id="footer">',
            # self.editbar(d),
            # self.credits(d),
            # self.showversion(d, **keywords),
            # u'</div>',

            # Post footer custom html
            self.emit_custom_html(self.cfg.page_footer2),
            ]
        return u'\n'.join(html)

    # RecentChanges ######################################################

    def recentchanges_entry(self, d):
        """
        Assemble a single recentchanges entry (table row)

        @param d: parameter dictionary
        @rtype: string
        @return: recentchanges entry html
        """
        _ = self.request.getText
        html = []
        html.append('<tr>\n')

        html.append('<td class="rcicon1">%(icon_html)s</td>\n' % d)

        html.append('<td class="rcpagelink">%(pagelink_html)s</td>\n' % d)

        html.append('<td class="rctime">')
        if d['time_html']:
            html.append("%(time_html)s" % d)
        html.append('</td>\n')

        html.append('<td class="rcicon2">%(info_html)s</td>\n' % d)

        html.append('<td class="rceditor">')
        if d['editors']:
            html.append('<br>'.join(d['editors']))
        html.append('</td>\n')

        html.append('<td class="rccomment">')
        if d['comments']:
            if d['changecount'] > 1:
                notfirst = 0
                for comment in d['comments']:
                    html.append('%s<tt>#%02d</tt>&nbsp;%s' % (
                        notfirst and '<br>' or '', comment[0], comment[1]))
                    notfirst = 1
            else:
                comment = d['comments'][0]
                html.append('%s' % comment[1])
        html.append('</td>\n')

        html.append('</tr>\n')

        return ''.join(html)

    def recentchanges_daybreak(self, d):
        """
        Assemble a rc daybreak indication (table row)

        @param d: parameter dictionary
        @rtype: string
        @return: recentchanges daybreak html
        """
        if d['bookmark_link_html']:
            set_bm = '&nbsp; %(bookmark_link_html)s' % d
        else:
            set_bm = ''
        return ('<tr class="rcdaybreak"><td colspan="%d">'
                '<strong>%s</strong>'
                '%s'
                '</td></tr>\n') % (6, d['date'], set_bm)

    def recentchanges_header(self, d):
        """
        Assemble the recentchanges header (intro + open table)

        @param d: parameter dictionary
        @rtype: string
        @return: recentchanges header html
        """
        _ = self.request.getText

        # Should use user interface language and direction
        html = '<div class="recentchanges"%s>\n' % self.ui_lang_attr()
        html += '<div>\n'
        page = d['page']
        if self.shouldUseRSS(page):
            link = [
                u'<div class="rcrss">',
                self.request.formatter.url(1, self.rsshref(page)),
                self.request.formatter.rawHTML(self.make_icon("rss")),
                self.request.formatter.url(0),
                u'</div>',
                ]
            html += ''.join(link)
        html += '<p>'
        # Add day selector
        if d['rc_days']:
            days = []
            for day in d['rc_days']:
                if day == d['rc_max_days']:
                    days.append('<strong>%d</strong>' % day)
                else:
                    days.append(
                        wikiutil.link_tag(self.request,
                            '%s?max_days=%d' % (d['q_page_name'], day),
                            str(day),
                            self.request.formatter, rel='nofollow'))
            days = ' | '.join(days)
            html += (_("Show %s days.") % (days, ))

        if d['rc_update_bookmark']:
            html += " %(rc_update_bookmark)s %(rc_curr_bookmark)s" % d

        html += '</p>\n</div>\n'

        html += '<table>\n'
        return html

    def recentchanges_footer(self, d):
        """
        Assemble the recentchanges footer (close table)

        @param d: parameter dictionary
        @rtype: string
        @return: recentchanges footer html
        """
        _ = self.request.getText
        html = ''
        html += '</table>\n'
        if d['rc_msg']:
            html += "<br>%(rc_msg)s\n" % d
        html += '</div>\n'
        return html

    # Language stuff ####################################################

    def ui_lang_attr(self):
        """Generate language attributes for user interface elements

        User interface elements use the user language (if any), kept in
        request.lang.

        @rtype: string
        @return: lang and dir html attributes
        """
        lang = self.request.lang
        return ' lang="%s" dir="%s"' % (lang, i18n.getDirection(lang))

    def content_lang_attr(self):
        """Generate language attributes for wiki page content

        Page content uses the page language or the wiki default language.

        @rtype: string
        @return: lang and dir html attributes
        """
        lang = self.request.content_lang
        return ' lang="%s" dir="%s"' % (lang, i18n.getDirection(lang))

    def add_msg(self, msg, msg_class=None):
        """ Adds a message to a list which will be used to generate status
        information.

        @param msg: additional message
        @param msg_class: html class for the div of the additional message.
        """
        if not msg_class:
            msg_class = 'dialog'
        if self._send_title_called:
            import traceback
            logging.warning("Calling add_msg() after send_title(): no message can be added.")
            logging.info('\n'.join(['Call stack for add_msg():'] + traceback.format_stack()))

            return
        self._status.append((msg, msg_class))

    # stuff from wikiutil.py
    def send_title(self, text, **keywords):
        """
        Output the page header (and title).

        @param text: the title text
        @keyword page: the page instance that called us - using this is more efficient than using pagename..
        @keyword pagename: 'PageName'
        @keyword print_mode: 1 (or 0)
        @keyword editor_mode: 1 (or 0)
        @keyword media: css media type, defaults to 'screen'
        @keyword allow_doubleclick: 1 (or 0)
        @keyword html_head: additional <head> code
        @keyword body_attr: additional <body> attributes
        @keyword body_onload: additional "onload" JavaScript code
        """
        request = self.request
        _ = request.getText
        rev = request.rev

        if keywords.has_key('page'):
            page = keywords['page']
            pagename = page.page_name
        else:
            pagename = keywords.get('pagename', '')
            page = Page(request, pagename)
        if keywords.get('msg', ''):
            raise DeprecationWarning("Using send_page(msg=) is deprecated! Use theme.add_msg() instead!")
        scriptname = request.script_root

        # get name of system pages
        page_front_page = wikiutil.getFrontPage(request).page_name
        page_help_contents = wikiutil.getLocalizedPage(request, 'HelpContents').page_name
        page_title_index = wikiutil.getLocalizedPage(request, 'TitleIndex').page_name
        page_site_navigation = wikiutil.getLocalizedPage(request, 'SiteNavigation').page_name
        page_word_index = wikiutil.getLocalizedPage(request, 'WordIndex').page_name
        page_help_formatting = wikiutil.getLocalizedPage(request, 'HelpOnFormatting').page_name
        page_find_page = wikiutil.getLocalizedPage(request, 'FindPage').page_name
        home_page = wikiutil.getInterwikiHomePage(request) # sorry theme API change!!! Either None or tuple (wikiname,pagename) now.
        page_parent_page = getattr(page.getParentPage(), 'page_name', None)

        # set content_type, including charset, so web server doesn't touch it:
        request.content_type = "text/html; charset=%s" % (config.charset, )

        # Prepare the HTML <head> element
        user_head = [request.cfg.html_head]

        # include charset information - needed for moin_dump or any other case
        # when reading the html without a web server
        user_head.append('''<meta http-equiv="Content-Type" content="%s;charset=%s">\n''' % (page.output_mimetype, page.output_charset))

        meta_keywords = request.getPragma('keywords')
        meta_desc = request.getPragma('description')
        if meta_keywords:
            user_head.append('<meta name="keywords" content="%s">\n' % wikiutil.escape(meta_keywords, 1))
        if meta_desc:
            user_head.append('<meta name="description" content="%s">\n' % wikiutil.escape(meta_desc, 1))

        #  add meta statement if user has doubleclick on edit turned on or it is default
        if (pagename and keywords.get('allow_doubleclick', 0) and
            not keywords.get('print_mode', 0) and
            request.user.edit_on_doubleclick):
            if request.user.may.write(pagename): # separating this gains speed
                user_head.append('<meta name="edit_on_doubleclick" content="%s">\n' % (request.script_root or '/'))

        # search engine precautions / optimization:
        # if it is an action or edit/search, send query headers (noindex,nofollow):
        if request.query_string:
            user_head.append(request.cfg.html_head_queries)
        elif request.method == 'POST':
            user_head.append(request.cfg.html_head_posts)
        # we don't want to have BadContent stuff indexed:
        elif pagename in ['BadContent', 'LocalBadContent', ]:
            user_head.append(request.cfg.html_head_posts)
        # if it is a special page, index it and follow the links - we do it
        # for the original, English pages as well as for (the possibly
        # modified) frontpage:
        elif pagename in [page_front_page, request.cfg.page_front_page,
                          page_title_index, 'TitleIndex',
                          page_find_page, 'FindPage',
                          page_site_navigation, 'SiteNavigation',
                          'RecentChanges', ]:
            user_head.append(request.cfg.html_head_index)
        # if it is a normal page, index it, but do not follow the links, because
        # there are a lot of illegal links (like actions) or duplicates:
        else:
            user_head.append(request.cfg.html_head_normal)

        if 'pi_refresh' in keywords and keywords['pi_refresh']:
            user_head.append('<meta http-equiv="refresh" content="%d;URL=%s">' % keywords['pi_refresh'])

        # output buffering increases latency but increases throughput as well
        output = []
        # later: <html xmlns=\"http://www.w3.org/1999/xhtml\">
        #<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
        output.append("""\
<!DOCTYPE html>
<!-- 
Template Name: Metronic - Responsive Admin Dashboard Template build with Twitter Bootstrap 3.3.5
Version: 4.1.0
Author: KeenThemes
Website: http://www.keenthemes.com/
Contact: support@keenthemes.com
Follow: www.twitter.com/keenthemes
Like: www.facebook.com/keenthemes
Purchase: http://themeforest.net/item/metronic-responsive-admin-dashboard-template/4021469?ref=keenthemes
License: You must have a valid license purchased only from themeforest(the above link) in order to legally use the theme for your project.
-->
<!--[if IE 8]> <html lang="en" class="ie8 no-js"> <![endif]-->
<!--[if IE 9]> <html lang="en" class="ie9 no-js"> <![endif]-->
<!--[if !IE]><!-->
<html lang="en" class="no-js">
<!--<![endif]-->
<!-- BEGIN HEAD -->
<head>
%s
%s
%s

<!-- BEGIN GLOBAL MANDATORY STYLES -->
<link href="https://fonts.googleapis.com/css?family=Open+Sans:400,300,600,700&subset=all" rel="stylesheet" type="text/css"/>
<link href="/master/moin_static195/metronic/assets/global/plugins/font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css"/>
<link href="/master/moin_static195/metronic/assets/global/plugins/simple-line-icons/simple-line-icons.min.css" rel="stylesheet" type="text/css"/>
<link href="/master/moin_static195/metronic/assets/global/plugins/bootstrap/css/bootstrap.min.css" rel="stylesheet" type="text/css"/>
<link href="/master/moin_static195/metronic/assets/global/plugins/uniform/css/uniform.default.css" rel="stylesheet" type="text/css"/>
<link href="/master/moin_static195/metronic/assets/global/plugins/bootstrap-switch/css/bootstrap-switch.min.css" rel="stylesheet" type="text/css"/>
<!-- END GLOBAL MANDATORY STYLES -->
<!-- BEGIN PAGE LEVEL PLUGIN STYLES -->
<link href="/master/moin_static195/metronic/assets/global/plugins/bootstrap-daterangepicker/daterangepicker-bs3.css" rel="stylesheet" type="text/css"/>
<link href="/master/moin_static195/metronic/assets/global/plugins/fullcalendar/fullcalendar.min.css" rel="stylesheet" type="text/css"/>
<link href="/master/moin_static195/metronic/assets/global/plugins/jqvmap/jqvmap/jqvmap.css" rel="stylesheet" type="text/css"/>
<!-- END PAGE LEVEL PLUGIN STYLES -->
<!-- BEGIN PAGE STYLES -->
<link href="/master/moin_static195/metronic/assets/admin/pages/css/tasks.css" rel="stylesheet" type="text/css"/>
<!-- END PAGE STYLES -->
<!-- BEGIN THEME STYLES -->
<link href="/master/moin_static195/metronic/assets/global/css/components.css" id="style_components" rel="stylesheet" type="text/css"/>
<link href="/master/moin_static195/metronic/assets/global/css/plugins.css" rel="stylesheet" type="text/css"/>
<link href="/master/moin_static195/metronic/assets/admin/layout/css/layout.css" rel="stylesheet" type="text/css"/>
<link href="/master/moin_static195/metronic/assets/admin/layout/css/themes/darkblue.css" rel="stylesheet" type="text/css" id="style_color"/>
<link href="/master/moin_static195/metronic/assets/admin/layout/css/custom.css" rel="stylesheet" type="text/css"/>
<!-- END THEME STYLES -->
<link rel="shortcut icon" href="favicon.ico"/>
""" % (
            ''.join(user_head),
            self.html_head({
                'page': page,
                'title': text,
                'sitename': request.cfg.html_pagetitle or request.cfg.sitename,
                'print_mode': keywords.get('print_mode', False),
                'media': keywords.get('media', 'screen'),
            }),
            keywords.get('html_head', ''),
        ))

        # Links
        output.append('<link rel="Start" href="%s">\n' % request.href(page_front_page))
        if pagename:
            output.append('<link rel="Alternate" title="%s" href="%s">\n' % (
                    _('Wiki Markup'), request.href(pagename, action='raw')))
            output.append('<link rel="Alternate" media="print" title="%s" href="%s">\n' % (
                    _('Print View'), request.href(pagename, action='print')))

            # !!! currently disabled due to Mozilla link prefetching, see
            # http://www.mozilla.org/projects/netlib/Link_Prefetching_FAQ.html
            #~ all_pages = request.getPageList()
            #~ if all_pages:
            #~     try:
            #~         pos = all_pages.index(pagename)
            #~     except ValueError:
            #~         # this shopuld never happend in theory, but let's be sure
            #~         pass
            #~     else:
            #~         request.write('<link rel="First" href="%s/%s">\n' % (request.script_root, quoteWikinameURL(all_pages[0]))
            #~         if pos > 0:
            #~             request.write('<link rel="Previous" href="%s/%s">\n' % (request.script_root, quoteWikinameURL(all_pages[pos-1])))
            #~         if pos+1 < len(all_pages):
            #~             request.write('<link rel="Next" href="%s/%s">\n' % (request.script_root, quoteWikinameURL(all_pages[pos+1])))
            #~         request.write('<link rel="Last" href="%s/%s">\n' % (request.script_root, quoteWikinameURL(all_pages[-1])))

            if page_parent_page:
                output.append('<link rel="Up" href="%s">\n' % request.href(page_parent_page))

        # write buffer because we call AttachFile
        request.write(''.join(output))
        output = []

        # XXX maybe this should be removed completely. moin emits all attachments as <link rel="Appendix" ...>
        # and it is at least questionable if this fits into the original intent of rel="Appendix".
        if pagename and request.user.may.read(pagename):
            from MoinMoin.action import AttachFile
            AttachFile.send_link_rel(request, pagename)

        output.extend([
            '<link rel="Search" href="%s">\n' % request.href(page_find_page),
            '<link rel="Index" href="%s">\n' % request.href(page_title_index),
            '<link rel="Glossary" href="%s">\n' % request.href(page_word_index),
            '<link rel="Help" href="%s">\n' % request.href(page_help_formatting),
                      ])

        output.append("""\
</head>
<!-- END HEAD -->
<!-- BEGIN BODY -->
<!-- DOC: Apply "page-header-fixed-mobile" and "page-footer-fixed-mobile" class to body element to force fixed header or footer in mobile devices -->
<!-- DOC: Apply "page-sidebar-closed" class to the body and "page-sidebar-menu-closed" class to the sidebar menu element to hide the sidebar by default -->
<!-- DOC: Apply "page-sidebar-hide" class to the body to make the sidebar completely hidden on toggle -->
<!-- DOC: Apply "page-sidebar-closed-hide-logo" class to the body element to make the logo hidden on sidebar toggle -->
<!-- DOC: Apply "page-sidebar-hide" class to body element to completely hide the sidebar on sidebar toggle -->
<!-- DOC: Apply "page-sidebar-fixed" class to have fixed sidebar -->
<!-- DOC: Apply "page-footer-fixed" class to the body element to have fixed footer -->
<!-- DOC: Apply "page-sidebar-reversed" class to put the sidebar on the right side -->
<!-- DOC: Apply "page-full-width" class to the body element to have full width page without the sidebar menu -->
""")
        request.write(''.join(output))
        output = []

        # start the <body>
        bodyattr = []
        if keywords.has_key('body_attr'):
            bodyattr.append(' ')
            bodyattr.append(keywords['body_attr'])

        # Set body to the user interface language and direction
        bodyattr.append(' %s' % self.ui_lang_attr())

        body_onload = keywords.get('body_onload', '')
        if body_onload:
            bodyattr.append(''' onload="%s"''' % body_onload)
        output.append('\n<body class="page-header-fixed page-quick-sidebar-over-content page-sidebar-closed-hide-logo page-container-bg-solid" %s>\n' % ''.join(bodyattr))

        # Output -----------------------------------------------------------

        # If in print mode, start page div and emit the title
        if keywords.get('print_mode', 0):
            d = {
                'title_text': text,
                'page': page,
                'page_name': pagename or '',
                'rev': rev,
            }
            request.themedict = d
            output.append(self.startPage())
            output.append(self.interwiki(d))
            output.append(self.title(d))

        # In standard mode, emit theme.header
        else:
            exists = pagename and page.exists(includeDeleted=True)
            # prepare dict for theme code:
            d = {
                'theme': self.name,
                'script_name': scriptname,
                'title_text': text,
                'logo_string': request.cfg.logo_string,
                'site_name': request.cfg.sitename,
                'page': page,
                'rev': rev,
                'pagesize': pagename and page.size() or 0,
                # exists checked to avoid creation of empty edit-log for non-existing pages
                'last_edit_info': exists and page.lastEditInfo() or '',
                'page_name': pagename or '',
                'page_find_page': page_find_page,
                'page_front_page': page_front_page,
                'home_page': home_page,
                'page_help_contents': page_help_contents,
                'page_help_formatting': page_help_formatting,
                'page_parent_page': page_parent_page,
                'page_title_index': page_title_index,
                'page_word_index': page_word_index,
                'user_name': request.user.name,
                'user_valid': request.user.valid,
                'msg': self._status,
                'trail': keywords.get('trail', None),
                # Discontinued keys, keep for a while for 3rd party theme developers
                'titlesearch': 'use self.searchform(d)',
                'textsearch': 'use self.searchform(d)',
                'navibar': ['use self.navibar(d)'],
                'available_actions': ['use self.request.availableActions(page)'],
            }

            # add quoted versions of pagenames
            newdict = {}
            for key in d:
                if key.startswith('page_'):
                    if not d[key] is None:
                        newdict['q_'+key] = wikiutil.quoteWikinameURL(d[key])
                    else:
                        newdict['q_'+key] = None
            d.update(newdict)
            request.themedict = d

            # now call the theming code to do the rendering
            if keywords.get('editor_mode', 0):
                output.append(self.editorheader(d))
            else:
                output.append(self.header(d))

        # emit it
        request.write(''.join(output))
        output = []
        self._send_title_called = True

    def send_footer(self, pagename, **keywords):
        """
        Output the page footer.

        @param pagename: WikiName of the page
        @keyword print_mode: true, when page is displayed in Print mode
        """
        request = self.request
        d = request.themedict




        # Emit end of page in print mode, or complete footer in standard mode
        if keywords.get('print_mode', 0):
            request.write(self.pageinfo(d['page']))
            request.write(self.endPage())
        else:
            request.write(self.footer(d, **keywords))
            request.write('''<!-- BEGIN FOOTER -->
<div class="page-footer">
    <div class="page-footer-inner" style="text-align:right">''')
            request.write(self.pageinfo(d['page']))
            request.write('''
    </div>
    <div class="scroll-to-top">
        <i class="icon-arrow-up"></i>
    </div>
</div>
<!-- END FOOTER -->''')
        request.write('''\
<!-- BEGIN JAVASCRIPTS(Load javascripts at bottom, this will reduce page load time) -->
<!-- BEGIN CORE PLUGINS -->
<!--[if lt IE 9]>
<script src="/master/moin_static195/metronic/assets/global/plugins/respond.min.js"></script>
<script src="/master/moin_static195/metronic/assets/global/plugins/excanvas.min.js"></script> 
<![endif]-->
<script src="/master/moin_static195/metronic/assets/global/plugins/jquery.min.js" type="text/javascript"></script>
<script src="/master/moin_static195/metronic/assets/global/plugins/jquery-migrate.min.js" type="text/javascript"></script>
<!-- IMPORTANT! Load jquery-ui.min.js before bootstrap.min.js to fix bootstrap tooltip conflict with jquery ui tooltip -->
<script src="/master/moin_static195/metronic/assets/global/plugins/jquery-ui/jquery-ui.min.js" type="text/javascript"></script>
<script src="/master/moin_static195/metronic/assets/global/plugins/bootstrap/js/bootstrap.min.js" type="text/javascript"></script>
<script src="/master/moin_static195/metronic/assets/global/plugins/bootstrap-hover-dropdown/bootstrap-hover-dropdown.min.js" type="text/javascript"></script>
<script src="/master/moin_static195/metronic/assets/global/plugins/jquery-slimscroll/jquery.slimscroll.min.js" type="text/javascript"></script>
<script src="/master/moin_static195/metronic/assets/global/plugins/jquery.blockui.min.js" type="text/javascript"></script>
<script src="/master/moin_static195/metronic/assets/global/plugins/jquery.cokie.min.js" type="text/javascript"></script>
<script src="/master/moin_static195/metronic/assets/global/plugins/uniform/jquery.uniform.min.js" type="text/javascript"></script>
<script src="/master/moin_static195/metronic/assets/global/plugins/bootstrap-switch/js/bootstrap-switch.min.js" type="text/javascript"></script>
<!-- END CORE PLUGINS -->
<!-- BEGIN PAGE LEVEL PLUGINS -->
<script src="/master/moin_static195/metronic/assets/global/plugins/jqvmap/jqvmap/jquery.vmap.js" type="text/javascript"></script>
<script src="/master/moin_static195/metronic/assets/global/plugins/jqvmap/jqvmap/maps/jquery.vmap.russia.js" type="text/javascript"></script>
<script src="/master/moin_static195/metronic/assets/global/plugins/jqvmap/jqvmap/maps/jquery.vmap.world.js" type="text/javascript"></script>
<script src="/master/moin_static195/metronic/assets/global/plugins/jqvmap/jqvmap/maps/jquery.vmap.europe.js" type="text/javascript"></script>
<script src="/master/moin_static195/metronic/assets/global/plugins/jqvmap/jqvmap/maps/jquery.vmap.germany.js" type="text/javascript"></script>
<script src="/master/moin_static195/metronic/assets/global/plugins/jqvmap/jqvmap/maps/jquery.vmap.usa.js" type="text/javascript"></script>
<script src="/master/moin_static195/metronic/assets/global/plugins/jqvmap/jqvmap/data/jquery.vmap.sampledata.js" type="text/javascript"></script>
<script src="/master/moin_static195/metronic/assets/global/plugins/flot/jquery.flot.min.js" type="text/javascript"></script>
<script src="/master/moin_static195/metronic/assets/global/plugins/flot/jquery.flot.resize.min.js" type="text/javascript"></script>
<script src="/master/moin_static195/metronic/assets/global/plugins/flot/jquery.flot.categories.min.js" type="text/javascript"></script>
<script src="/master/moin_static195/metronic/assets/global/plugins/jquery.pulsate.min.js" type="text/javascript"></script>
<script src="/master/moin_static195/metronic/assets/global/plugins/bootstrap-daterangepicker/moment.min.js" type="text/javascript"></script>
<script src="/master/moin_static195/metronic/assets/global/plugins/bootstrap-daterangepicker/daterangepicker.js" type="text/javascript"></script>
<!-- IMPORTANT! fullcalendar depends on jquery-ui.min.js for drag & drop support -->
<script src="/master/moin_static195/metronic/assets/global/plugins/fullcalendar/fullcalendar.min.js" type="text/javascript"></script>
<script src="/master/moin_static195/metronic/assets/global/plugins/jquery-easypiechart/jquery.easypiechart.min.js" type="text/javascript"></script>
<script src="/master/moin_static195/metronic/assets/global/plugins/jquery.sparkline.min.js" type="text/javascript"></script>
<!-- END PAGE LEVEL PLUGINS -->
<!-- BEGIN PAGE LEVEL SCRIPTS -->
<script src="/master/moin_static195/metronic/assets/global/scripts/metronic.js" type="text/javascript"></script>
<script src="/master/moin_static195/metronic/assets/admin/layout/scripts/layout.js" type="text/javascript"></script>
<script src="/master/moin_static195/metronic/assets/admin/layout/scripts/quick-sidebar.js" type="text/javascript"></script>
<script src="/master/moin_static195/metronic/assets/admin/layout/scripts/demo.js" type="text/javascript"></script>
<script src="/master/moin_static195/metronic/assets/admin/pages/scripts/index.js" type="text/javascript"></script>
<script src="/master/moin_static195/metronic/assets/admin/pages/scripts/tasks.js" type="text/javascript"></script>
<!-- END PAGE LEVEL SCRIPTS -->
<script>
jQuery(document).ready(function() {    
   Metronic.init(); // init metronic core componets
   Layout.init(); // init layout
   QuickSidebar.init(); // init quick sidebar
Demo.init(); // init demo features
   Index.init();   
   Index.initDashboardDaterange();
   Index.initJQVMAP(); // init index page's custom scripts
   Index.initCalendar(); // init index page's custom scripts
   Index.initCharts(); // init index page's custom scripts
   Index.initChat();
   Index.initMiniCharts();
   Tasks.initDashboardWidget();
});
</script>
<!-- END JAVASCRIPTS -->
''')

    # stuff moved from request.py
    def send_closing_html(self):
        """ generate timing info html and closing html tag,
            everyone calling send_title must call this at the end to close
            the body and html tags.
        """
        request = self.request

        # as this is the last chance to emit some html, we stop the clocks:
        request.clock.stop('run')
        request.clock.stop('total')

        # Close html code
        if request.cfg.show_timings and request.action != 'print':
            request.write('<ul id="timings">\n')
            for t in request.clock.dump():
                request.write('<li>%s</li>\n' % t)
            request.write('</ul>\n')
        #request.write('<!-- auth_method == %s -->' % repr(request.user.auth_method))
        # request.write('</body>\n</html>\n\n')
        request.write('''\
</body>
<!-- END BODY -->
</html>''')

    def sidebar(self, d, **keywords):
        """ Display page called SideBar as an additional element on every page

        @param d: parameter dictionary
        @rtype: string
        @return: sidebar html
        """

        # Check which page to display, return nothing if doesn't exist.
        sidebar = self.request.getPragma('sidebar', u'SideBar')
        page = Page(self.request, sidebar)
        if not page.exists():
            return u""
        # Capture the page's generated HTML in a buffer.
        buffer = StringIO.StringIO()
        self.request.redirect(buffer)
        try:
            page.send_page(content_only=1, content_id="sidebar")
        finally:
            self.request.redirect()
        return u'<div class="sidebar">%s</div>' % buffer.getvalue()


class ThemeNotFound(Exception):
    """ Thrown if the supplied theme could not be found anywhere """

def load_theme(request, theme_name=None):
    """ Load a theme for this request.

    @param request: moin request
    @param theme_name: the name of the theme
    @type theme_name: str
    @rtype: Theme
    @return: a theme initialized for the request
    """
    if theme_name is None or theme_name == '<default>':
        theme_name = request.cfg.theme_default

    try:
        Theme = wikiutil.importPlugin(request.cfg, 'theme', theme_name, 'Theme')
    except wikiutil.PluginMissingError:
        raise ThemeNotFound(theme_name)

    return Theme(request)

def load_theme_fallback(request, theme_name=None):
    """ Try loading a theme, falling back to defaults on error.

    @param request: moin request
    @param theme_name: the name of the theme
    @type theme_name: str
    @rtype: int
    @return: A statuscode for how successful the loading was
             0 - theme was loaded
             1 - fallback to default theme
             2 - serious fallback to builtin theme
    """
    fallback = 0
    try:
        request.theme = load_theme(request, theme_name)
    except ThemeNotFound:
        fallback = 1
        try:
            request.theme = load_theme(request, request.cfg.theme_default)
        except ThemeNotFound:
            fallback = 2
            from MoinMoin.theme.modern import Theme
            request.theme = Theme(request)
