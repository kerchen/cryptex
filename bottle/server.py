from bottle import (get, redirect, request, route, run, ServerAdapter,
                    static_file, template, TEMPLATE_PATH)
from cheroot import wsgi
from cheroot.ssl.builtin import BuiltinSSLAdapter
import logging
import os
import ssl

# Note: any modules that supply bottle functionality need to be imported
# here even though they aren't used directly.
import shared_cfg
import authentication
import navigation
import manage_passwords


log = logging.getLogger(__name__)


# Tell bottle to look in these directories for templates.
RBB_EXPORT_DIRECTORY = 'web-ui_exported'
GENERATED_TEMPLATE_DIRECTORY = 'generated_templates'
TEMPLATE_PATH.append('./{0}/'.format(RBB_EXPORT_DIRECTORY))
TEMPLATE_PATH.append('./{0}/'.format(GENERATED_TEMPLATE_DIRECTORY))


@get('/css/<filename:re:.*\.css>')
def send_css(filename):
    global RBB_EXPORT_DIRECTORY
    return static_file(filename, root='{0}/css'.format(RBB_EXPORT_DIRECTORY))


@get('/fonts/<filename:re:.*\.(eot|svg|ttf|woff)>')
def send_font(filename):
    global RBB_EXPORT_DIRECTORY
    return static_file(filename, root='{0}/fonts'.format(RBB_EXPORT_DIRECTORY))


@get('/images/<filename:re:.*\.(jpg|png)>')
def send_image(filename):
    global RBB_EXPORT_DIRECTORY
    return static_file(filename, root='{0}/images'.format(RBB_EXPORT_DIRECTORY))


@get('/js/<filename:re:.*\.js>')
def send_js(filename):
    global RBB_EXPORT_DIRECTORY
    return static_file(filename, root='{0}/js'.format(RBB_EXPORT_DIRECTORY))


@route('/')
def default():
    if shared_cfg.validate_session(request):
        return redirect("/manage")
    elif shared_cfg.is_session_active():
        return template("session-error.html")
    elif request.get_cookie(shared_cfg.SESSION_COOKIE_NAME) is not None:
        return template("session-error.html")
    elif shared_cfg.is_in_keyboard_mode():
        return template("keyboard-mode.html")
    else:
        return redirect("/login")


def generate_template_from_body(page_filename):
    """
        Copies the body of page_filename (which is assumed to be an HTML
        document) into a separate bottle template file. That file is
        created in the generated template directory and its name is
        returned by the function.
    """

    global GENERATED_TEMPLATE_DIRECTORY, RBB_EXPORT_DIRECTORY

    in_body = False
    if not os.path.exists(GENERATED_TEMPLATE_DIRECTORY):
        os.mkdir(GENERATED_TEMPLATE_DIRECTORY)

    tpl_filename = '{0}_body.tpl'.format(os.path.splitext(page_filename)[0])
    tpl_file = open(os.path.join(GENERATED_TEMPLATE_DIRECTORY, tpl_filename),
                    'wb')
    with open(os.path.join(RBB_EXPORT_DIRECTORY, page_filename), 'rb') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line.startswith("<body>"):
                in_body = True
            elif in_body:
                if stripped_line.startswith("</body>"):
                    break
                else:
                    tpl_file.write(line)

    tpl_file.close()
    return tpl_filename


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
