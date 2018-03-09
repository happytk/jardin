# -*- coding: utf-8 -
import sys
import os
sys.path.insert(0, os.path.join(os.path.abspath('.'), 'lib'))
os.environ['MOIN'] = os.path.join(os.path.abspath('.'), 'lib')
from MoinMoin.web.serving import make_application, run_server

app = make_application()

if __name__ == "__main__":
    run_server(hostname='localhost', port=8080,
               docs=True,
               debug='off',
               user=None, group=None,
               threaded=True)