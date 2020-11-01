from app import app
from flask import render_template, request, redirect, flash
import admins

# Admin aloitus
@app.route("/hallinta")
def admin():
    return render_template("adlogin.html", login="yes")

# Admin päävalikko
@app.route("/admenu")
def ad_menu():
    if admins.admin_id() == 0:
        return render_template("adlogin.html", login="yes")
    else:
        return render_template("admenu.html")


# Admin login
@app.route("/adlogin", methods=["get","post"])
def ad_login():
    if request.method == "GET":
        return render_template("adlogin.html", login="yes")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if admins.login(username,password):
            return redirect("/admenu")
        else:
            error = "Väärä tunnus tai salasana"
            return render_template("adlogin.html", login="yes", error=error)

# Admin login hinnat
@app.route("/adloginh", methods=["get","post"])
def ad_loginh():
    if request.method == "GET":
        return render_template("adloginh.html", login="yes")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if admins.login(username,password):
            return redirect("/hinnat")
        else:
            error = "Väärä tunnus tai salasana"
            return render_template("adloginh.html", login="yes", error=error)

# Admin login varaukset
@app.route("/adloginv", methods=["get","post"])
def ad_loginv():
    if request.method == "GET":
        return render_template("adloginv.html", login="yes")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if admins.login(username,password):
            return redirect("/varaukset")
        else:
            error = "Väärä tunnus tai salasana"
            return render_template("adloginv.html", login="yes", error=error)

# Admin login vapaat
@app.route("/adloginvap", methods=["get","post"])
def ad_loginvap():
    if request.method == "GET":
        return render_template("adloginvap.html", login="yes")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if admins.login(username,password):
            return redirect("/vapaat")
        else:
            error = "Väärä tunnus tai salasana"
            return render_template("adloginvap.html", login="yes", error=error)

# Admin logout
@app.route("/adlogout")
def ad_logout():
    admins.logout()
    return render_template("adlogout.html", login="yes")

# Admin logout
@app.route("/adlogouth")
def ad_logouth():
    admins.logout()
    return render_template("adlogouth.html", login="yes")

# Admin logout
@app.route("/adlogoutv")
def ad_logoutv():
    admins.logout()
    return render_template("adlogoutv.html", login="yes")

# Admin logout
@app.route("/adlogoutvap")
def ad_logoutvap():
    admins.logout()
    return render_template("adlogoutvap.html", login="yes")

# Uusi admin käyttäjä
@app.route("/adregister", methods=["get","post"])
def ad_register():
    if admins.admin_id() == 0:
        return render_template("adlogin.html", login="yes")
    else:
        if request.method == "GET":
            return render_template("adregister.html")
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            if admins.register(username,password):
                return redirect("/admenu")
            else:
                return render_template("error.html",message="Rekisteröinti ei onnistunut")

def isBlank (myString):
    return not (myString and myString.strip())

