import bottle
from cheroot import wsgi
from cheroot.ssl.builtin import BuiltinSSLAdapter
import ssl

import shared_cfg
import authentication


@bottle.route('/<filename:path>')
def send_static(filename):
    return bottle.static_file(filename, root="web-root")


@bottle.route('/')
def default():
    if not shared_cfg.db_conn:
        bottle.redirect("/login")
    else:
        bottle.redirect("/index.html")


@bottle.route('/lock')
def lock():
    print("Locking the whole thing down")
    bottle.redirect("/lock.html")


@bottle.route('/activate')
def lock():
    print("Activating the device")
    bottle.redirect("/activate.html")


@bottle.route('/master-pass')
def lock():
    print("Changing master password")
    bottle.redirect("/master-pass.html")


@bottle.route('/manage')
def lock():
    print("Managing passwords")
    bottle.redirect("/manage.html")


@bottle.post('/main_menu')
def do_main_menu():
    if bottle.request.forms.get("lock"):
        bottle.redirect("/lock")
    elif bottle.request.forms.get("activate"):
        bottle.redirect("/activate")
    elif bottle.request.forms.get("master_pass"):
        bottle.redirect("/master-pass")
    elif bottle.request.forms.get("manage"):
        bottle.redirect("/manage")


# Create our own sub-class of Bottle's ServerAdapter
# so that we can specify SSL. Using just server='cherrypy'
# uses the default cherrypy server, which doesn't use SSL
class SSLCherryPyServer(bottle.ServerAdapter):
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
    bottle.run(host='0.0.0.0',
               port=443,
               debug=debug,
               quiet=not debug,
               server=SSLCherryPyServer)
