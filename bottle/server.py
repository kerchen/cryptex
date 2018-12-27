from bottle import (get, redirect, request, route, run, ServerAdapter,
                    static_file, template)
from cheroot import wsgi
from cheroot.ssl.builtin import BuiltinSSLAdapter
import logging
import ssl

import shared_cfg
import authentication
import navigation
import manage_passwords
import edit_entry


log = logging.getLogger(__name__)


@get('/css/<filename:re:.*\.css>')
def send_css(filename):
    return static_file(filename, root='web-ui_exported/css')


@get('/fonts/<filename:re:.*\.(eot|svg|ttf|woff)>')
def send_font(filename):
    return static_file(filename, root='web-ui_exported/fonts')


@get('/images/<filename:re:.*\.(jpg|png)>')
def send_image(filename):
    return static_file(filename, root='web-ui_exported/images')


@get('/js/<filename:re:.*\.js>')
def send_js(filename):
    return static_file(filename, root='web-ui_exported/js')


@route('/')
def default():
    if shared_cfg.validate_session(request):
        return redirect("/manage")
    elif shared_cfg.is_session_active():
        return template("session_mismatch.tpl", title="Cryptex Session Active")
    elif request.get_cookie(shared_cfg.SESSION_COOKIE_NAME) is not None:
        return template("session_timeout.tpl", title="Cryptex Session Timed Out")
    elif shared_cfg.is_in_keyboard_mode():
        return template("activate_keyboard_mode.tpl", title="Keyboard Mode")
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
            log.info("Stopping web server.")
            server.stop()


def run_web_server(debug):
    run(host='0.0.0.0',
           port=443,
           debug=debug,
           quiet=not debug,
           server=SSLCherryPyServer)
