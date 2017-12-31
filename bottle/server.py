from bottle import get, post, request, route, run, static_file

import shared_cfg

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

#@route('/favicon.ico')
#def server_static(filename):
    #return static_file(filename, root='/home/pi/bottle/assets')

def run_web_server(debug):
    run(host='0.0.0.0', port=80, debug=debug, quiet=not debug)
