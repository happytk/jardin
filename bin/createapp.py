# -*- coding: utf-8 -
import sys
import os
sys.path.insert(0, os.path.join(os.path.abspath('.'), 'lib'))
os.environ['MOIN'] = os.path.join(os.path.abspath('.'), 'lib')
from MoinMoin.web.serving import make_application

app = make_application()
