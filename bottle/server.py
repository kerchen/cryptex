from bottle import (get, post, route, response, run, redirect, request,
                    static_file, ServerAdapter, default_app)
from cheroot import wsgi
from cheroot.ssl.builtin import BuiltinSSLAdapter
import os
import ssl

import db_setup
import shared_cfg


@route('/<filename:path>')
def send_static(filename):
    return static_file(filename, root="web-root")


@route('/')
def default():
    if not shared_cfg.db_conn:
        redirect("/login")
    else:
        redirect("/index.html")


def confirm_password_form(retry):
    form = '<form action="/first-time-setup" method="post">'
    if retry:
        form += "Entered passwords did not match. Please try again.</br>"
    form += '''
                Password database does not exist. Creating new one.</br>
                Password: <input name="password" type="password"/> </br>
                Re-enter Password: <input name="password2" type="password" />
                <input value="Create" type="submit" />
                </form>
            '''
    return form


@get('/first-time-setup')
def first_time_setup(retry=""):
    if not shared_cfg.db_conn:
        if not os.path.exists(shared_cfg.encrypted_db_filename):
            return confirm_password_form(False)
    redirect("/")


@get('/first-time-setup-retry')
def first_time_setup_retry():
    if not shared_cfg.db_conn:
        if not os.path.exists(shared_cfg.encrypted_db_filename):
            return confirm_password_form(True)
    redirect("/")


@post('/first-time-setup')
def do_first_time_setup():
    print("In do_first_time_setup()")
    password = request.forms.get('password')
    password2 = request.forms.get('password2')
    if password == password2:
        shared_cfg.cv.acquire()
        shared_cfg.db_conn = db_setup.open_encrypted_db(password)
        shared_cfg.cv.release()
        redirect("/")
    else:
       redirect("/first-time-setup-retry")


def enter_password_form(retry):
    form = '<form action="/login" method="post">'
    if retry:
        form += "Entered password didn't work. Please try again.</br>"
    form += '''
                Password: <input name="password" type="password" />
                <input value="Login" type="submit" />
                </form>
            '''
    return form


@get('/login-retry')
def login_retry():
    if not shared_cfg.db_conn:
        if not os.path.exists(shared_cfg.encrypted_db_filename):
            redirect("/first-time-setup")
            return ''
        return enter_password_form(True)
    redirect("/")


@get('/login')
def login():
    if not shared_cfg.db_conn:
        if not os.path.exists(shared_cfg.encrypted_db_filename):
            redirect("/first-time-setup")
            return ''
        return enter_password_form(False)
    redirect("/")


@post('/login')
def do_login():
    password = request.forms.get('password')
    shared_cfg.cv.acquire()
    shared_cfg.db_conn = db_setup.open_encrypted_db(password)
    shared_cfg.cv.release()
    if not shared_cfg.db_conn:
        redirect("/login-retry")
    else:
        redirect("/")

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


# @route('/favicon.ico')
# def server_static(filename):
    # return static_file(filename, root='/home/pi/bottle/assets')


def run_web_server(debug):
    run(host='0.0.0.0',
        port=443,
        debug=debug,
        quiet=not debug,
        server=SSLCherryPyServer)
