from app import app
from flask import render_template, request, redirect, flash
import admins

# Admin aloitus
@app.route("/admin")
def admin():
    return render_template("adlogin.html", login="yes")

# Admin päävalikko
@app.route("/admin/menu")
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
            return redirect("/admin/menu")
        else:
            error = "Väärä tunnus tai salasana"
            return render_template("adlogin.html", login="yes", error=error)

# Admin logout
@app.route("/adlogout")
def ad_logout():
    admins.logout()
    return render_template("adlogout.html", login="yes")

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
                return redirect("/admin/menu")
            else:
                return render_template("error.html",message="Rekisteröinti ei onnistunut")

def isBlank (myString):
    return not (myString and myString.strip())

