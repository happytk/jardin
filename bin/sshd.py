#!python
#-*-encoding: utf-8 -*-
import os
import sys
import signal
import logging
import flask
from werkzeug.serving import BaseRequestHandler, run_simple
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug import SharedDataMiddleware
from MoinMoin.util.daemon import Daemon
from MoinMoin.web.serving import make_application
from easy_attach import easy_attach_page


class RequestHandler(BaseRequestHandler):

    """
    A request-handler for WSGI, that overrides the default logging
    mechanisms to log via MoinMoin's logging framework.
    """
    server_version = "MoinMoin-Customized-by-happytk (development)"

    __shared = {}

    # override the logging functions
    def log_request(self, code='-', size='-'):
        self.log_message('"%s" %s %s',
                         self.requestline, code, size)

    def log_error(self, format, *args):
        self.log_message(format, *args)

    def log_message(self, format, *args):
        # logging.info("%s %s", self.address_string(), (format % args))
        pass


def spawn_app(shared, debug=False):
    app = flask.Flask(__name__, template_folder='templates',
                      static_folder='static')
    app.debug = debug
    app.register_blueprint(easy_attach_page,
                           url_prefix='/__moinfbp/easy_attach')

    @app.route('/robots.txt')
    def robots():
        return flask.send_from_directory(shared, 'robots.txt')

    @app.route('/favicon.ico')
    def favicon():
        return flask.send_from_directory(shared, 'favicon.ico')

    @app.route('/')
    def index():
        return flask.render_template('index.html')

    @app.route('/search')
    def search():
        return flask.render_template('search.html')
    # @app.route('/about')
    # def about():
    #     return 'hello'

    @app.errorhandler(404)
    def page_not_found(e):
        """Return a custom 404 error."""
        return flask.redirect(flask.url_for('index'))

    # from ercc import app as ercc_app

    # from MoinMoin.wsgiapp import application
    application = make_application(shared)
    application = DispatcherMiddleware(app, {
        '/archive':  application,
        '/ntuning':  application,
        '/amb':      application,
        '/mei':      application,
        '/master':   application,
        # '/ercc': ercc_app,
    })

    docs = {
        # '/webpub_amb': '/volume1/photo/webpub_amb',
        '/TK_dayone_photos': '/volume1/homes/me/dropbox/Apps/Day One/Journal.dayone/photos/',
        '/MEI_dayone_photos': '/volume1/homes/me/dropbox_happytk/Apps/Day One (1)/Journal.dayone/photos/',
        # '/static': '/volume1/moindev/lib/ercc_flask/ercc/static/',
    }
    return SharedDataMiddleware(application, docs)

if __name__ == "__main__":
    pidfile = "/volume1/moindev/moind.pid"
    if len(sys.argv) > 1 and sys.argv[1] in ['stop', 'restart']:
        try:
            pids = open(pidfile, "r").read()
            os.remove(pidfile)
        except IOError:
            print "pid file not found (server not running?)"
        else:
            try:
                os.kill(int(pids), signal.SIGTERM)
            except OSError:
                print "kill failed (server not running?)"

    if len(sys.argv) == 1 or \
            (len(sys.argv) == 2 and sys.argv[1] in ['start', 'restart']):
        hostname = '0.0.0.0'
        port = 8091
        debug = 'web'
        threaded = True
        ssl_context = ('/volume1/moindev/htdocs_ssl_data/ssl.crt',
                       '/volume1/moindev/htdocs_ssl_data/ssl.key')
        shared = '/volume1/moindev/lib/moindev/MoinMoinHtdocs'
        if debug == 'external':
            # no threading is better for debugging, the main (and only)
            # thread then will just terminate when an exception happens
            threaded = False

        application = spawn_app(shared, debug == 'web')

        kwargs = dict(hostname=hostname, port=port,
                      application=application,
                      threaded=threaded,
                      use_debugger=(debug == 'web'),
                      use_reloader=(debug == 'web'),
                      passthrough_errors=(debug == 'external'),
                      request_handler=RequestHandler,
                      ssl_context=ssl_context)
        if len(sys.argv) > 1 and sys.argv[1] in ['start', 'restart']:
            daemon = Daemon('moind', pidfile, run_simple, **kwargs)
            daemon.do_start()
        else:
            run_simple(**kwargs)
    # print 'hey'
    # print __name__
    # print sys.argv
