import bottle


@bottle.route('/lock')
def lock():
    print("Locking the whole thing down")
    bottle.redirect("/lock.html")


@bottle.route('/activate')
def activate():
    print("Activating the device")
    bottle.redirect("/activate.html")


@bottle.route('/master-pass')
def master_pass():
    print("Changing master password")
    bottle.redirect("/master-pass.html")


@bottle.route('/manage')
def manage():
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


