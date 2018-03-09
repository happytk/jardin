# -*- coding: iso-8859-1 -*-
"""
MoinMoin - a wiki engine in Python

@copyright: 2000-2006 by Juergen Hermann <jh@web.de>,
            2002-2009 MoinMoin:ThomasWaldmann
@license: GNU GPL, see COPYING for details.
"""



import os
import jinja2

TEMPLATE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'template')

def render_template(filename, **kwargs):
    path = os.path.join(TEMPLATE_PATH, filename)
    template = jinja2.Template(open(path, 'r').read().decode('utf8'))
    return template.render(**kwargs)
