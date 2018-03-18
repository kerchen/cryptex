from bottle import (redirect, request, route, run, ServerAdapter, static_file)
from cheroot import wsgi
from cheroot.ssl.builtin import BuiltinSSLAdapter
import ssl

import shared_cfg
import authentication
import main_screen


@route('/<filename:path>')
def send_static(filename):
    if shared_cfg.is_session_valid(request):
        return static_file(filename, root="web-root")
    else:
        return redirect("/login")


@route('/')
def default():
    if shared_cfg.is_session_valid(request):
        return redirect("/index.html")
    elif shared_cfg.is_session_active():
        return static_file("/session-mismatch.html", root="web-root")
    else:
        return redirect("/login")


# Create our own sub-class of Bottle's ServerAdapter
# so that we can specify SSL. Using just server='cherrypy'
# uses the default cherrypy server, which doesn't use SSL
class SSLCherryPyServer(ServerAdapter):
    def run(self, handler):
        server = wsgi.Server((self.host, self.port), handler)
        server.ssl_adapter = BuiltinSSLAdapter('./certs/device.crt',
                                               './certs/device.key')

        # By default, the server will allow negotiations with extremely old
        # protocols that are susceptible to attacks, so only allow TLSv1.2
        server.ssl_adapter.context.options |= ssl.OP_NO_TLSv1
        server.ssl_adapter.context.options |= ssl.OP_NO_TLSv1_1

        try:
            server.start()
        finally:
            server.stop()


def run_web_server(debug):
    run(host='0.0.0.0',
           port=443,
           debug=debug,
           quiet=not debug,
           server=SSLCherryPyServer)
