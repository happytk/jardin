# -*-encoding:utf-8-*-
import logging
import os
import jinja2
from MoinMoin import wikiutil
from MoinMoin.action.AttachFile import getAttachDir, _get_files


def getAttachUrl(pagename, filename, request, addts=0, do='get'):
    """ Get URL that points to attachment `filename` of page `pagename`.
        For upload url, call with do='upload_form'.
        Returns the URL to do the specified "do" action or None,
        if this action is not supported.
    """
    action = 'AttachFile'  # get_action(request, filename, do)
    if action:
        args = dict(action=action, do=do, target=filename)
        if do not in ['get', 'view',  # harmless
                      'modify',  # just renders the applet html, which has own ticket
                      'move',  # renders rename form, which has own ticket
                      ]:
            # create a ticket for the not so harmless operations
            # we need action= here because the current action (e.g. "show" page
            # with a macro AttachList) may not be the linked-to action, e.g.
            # "AttachFile". Also, AttachList can list attachments of another page,
            # thus we need to give pagename= also.
            args['ticket'] = wikiutil.createTicket(
                request,
                pagename=pagename,
                action=action
            )
        url = request.href(pagename, **args)
        return url


def get_attachments(pagename, request, attach_dir):
    files = _get_files(request, pagename)

    if files:
        lst = []
        for file in files:
            base, ext = os.path.splitext(file)
            fullpath = os.path.join(attach_dir, file)
            try:
                st = os.stat(fullpath)
            except OSError:
                logging.warn('cannot get filestat:' + fullpath)
                continue
            parmdict = {
                'file': wikiutil.escape(file),
                'fsize': "%.1f" % (float(st.st_size) / 1024),
                'fmtime': request.user.getFormattedDateTime(st.st_mtime),
                'ext': ext,
                'url': getAttachUrl(pagename, file, request),
            }
            lst.append(parmdict)
        lst = sorted(lst, key=lambda x: x['fmtime'], reverse=True)
        return lst
    else:
        return []


def send_body(pagename, request, editor=False):
    path = os.path.join(os.path.abspath(
        os.path.dirname(__file__)),
        'attachf.html')
    template = jinja2.Template(open(path, 'r').read().decode('utf8'))

    attach_dir = getAttachDir(request, pagename)
    files = get_attachments(pagename, request, attach_dir)
    request.write(template.render(
        editor=editor,
        pagename=pagename,
        may_write=request.user.may.write(pagename),
        config_name=request.cfg.config_name,
        attachment_path=attach_dir,
        files=files,
        script_root=request.script_root,
        static_url=request.cfg.url_prefix_static))


def execute(pagename, request):
    """ Main dispatcher for the 'AttachFile' action. """
    _ = request.getText

    # Use user interface language for this generated page
    request.setContentLanguage(request.lang)
    request.theme.send_title(
        _('Attachments for "%(pagename)s"') % {
            'pagename': pagename
        }, pagename=pagename)
    send_body(pagename, request)
    request.theme.send_footer(pagename)
    request.theme.send_closing_html()
