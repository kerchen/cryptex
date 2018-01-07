from bottle import (get, post, route, response, run, redirect, request,
                    static_file, ServerAdapter, default_app)
from cheroot import wsgi
from cheroot.ssl.builtin import BuiltinSSLAdapter
import ssl

import shared_cfg

@route('/<filename:path>')
def send_static(filename):
    return static_file(filename, root=".")

@route('/')
def default():
    redirect("/index.html")

@get('/login')
def login():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
    '''

def check_login(user, passwd):
    if user == 'paul' and passwd == 'pass':
        return True
    return False

@post('/login')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        shared_cfg.cv.acquire()
        shared_cfg.db_loaded = True
        shared_cfg.cv.release()
        return "<p>Your login information was correct.</p>"
    else:
        return "<p>Login failed.</p>"

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

#@route('/favicon.ico')
#def server_static(filename):
    #return static_file(filename, root='/home/pi/bottle/assets')

def run_web_server(debug):
    run(host='0.0.0.0',
        port=443,
        debug=debug,
        quiet=not debug,
        server=SSLCherryPyServer)
