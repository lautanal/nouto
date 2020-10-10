from app import app
from flask import render_template, request, redirect, flash
import users, areas, topics, messages, admins

@app.route("/admin")
def admin():
    return render_template("adindex.html")

# Admin päävalikko
@app.route("/admin/menu")
def ad_menu():
    admin_name = admins.get_adminname()
    return render_template("admenu.html", admin_name=admin_name)

# Keskustelualueiden hallinta
@app.route("/admin/areas")
def ad_list_areas():
    admin_name = admins.get_adminname()
    list = areas.get_areas_all()
    return render_template("adareas.html", admin_name=admin_name, areas=list)

# Viestiketjujen listaus
@app.route("/admin/topics/<int:area_id>")
def ad_list_topics(area_id):
    admin_name = admins.get_adminname()
    area_name = areas.get_areaname(area_id)
    list = topics.get_topics(area_id)
    return render_template("adtopics.html", admin_name=admin_name, area_id=area_id, area_name=area_name, topics=list)

# Viestien hallinta
@app.route("/admin/messages/<int:topic_id>")
def ad_list_messages(topic_id):
    admin_name = admins.get_adminname()
    area_id = topics.get_area_id(topic_id)
    area_name = areas.get_areaname(area_id)
    topic_name = topics.get_topicname(topic_id)
    list = messages.get_messages(topic_id)
    return render_template("admessages.html", admin_name=admin_name, area_id=area_id, area_name=area_name, topic_id=topic_id, topic_name=topic_name, count=len(list), messages=list)

# Uusi keskustelualue
@app.route("/admin/newarea")
def newarea():
    return render_template("newarea.html")

# Uuden keskustelualueen talletus tietokantaan
@app.route("/admin/areasend", methods=["post"])
def areasend():
    area_name = request.form["areaname"]
    hidden = request.form["hidden"]
    if isBlank(area_name) :
            return render_template("newarea.html",error="Tyhjä kenttä, keskustelualuetta ei aloitettu")
#            return render_template("error.html",message="Tyhjä kenttä, keskustelualuetta ei aloitettu")
    if areas.sendarea(area_name, hidden):
        return redirect("/admin/areas")
    else:
        return render_template("error.html",message="Viestiketjun talletus ei onnistunut")

# Viestin poisto (näkyvistä)
@app.route("/admin/messagedel/<int:message_id>")
def ad_deletem(message_id):
    topic_id = messages.get_topic_id(message_id)
    if messages.admin_delete(message_id):
        return redirect("/admin/messages/"+str(topic_id))
    else:
        return render_template("error.html",message="Viestin poisto ei onnistunut")

# Uusi viestiketju
@app.route("/admin/newtopic/<int:area_id>")
def ad_newtopic(area_id):
    return render_template("adnewtopic.html", area_id=area_id)

# Uuden viestiketjun talletus tietokantaan
@app.route("/admin/topicsend/<int:area_id>", methods=["post"])
def ad_topicsend(area_id):
    topic_name = request.form["topicname"]
    if isBlank(topic_name) :
            return render_template("adnewtopic.html", area_id=area_id, error="Tyhjä kenttä, viestiketjua ei aloitettu")
#            return render_template("error.html",message="Tyhjä kenttä, viestiketjua ei aloitettu")
    if topics.sendtopic(area_id, topic_name):
        return redirect("/admin/topics/"+str(area_id))
    else:
        return render_template("error.html",message="Viestiketjun talletus ei onnistunut")

# Admin login
@app.route("/adlogin", methods=["get","post"])
def ad_login():
    if request.method == "GET":
        return render_template("adlogin.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if admins.login(username,password):
            return redirect("/admin/menu")
        else:
            return render_template("error.html",message="Väärä tunnus tai salasana")

# Admin logout
@app.route("/adlogout")
def ad_logout():
    admins.logout()
    return redirect("/")

# Uusi admin käyttäjä
@app.route("/adregister", methods=["get","post"])
def ad_register():
    if request.method == "GET":
        return render_template("adregister.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if admins.register(username,password):
            return redirect("/admin/areas")
        else:
            return render_template("error.html",message="Rekisteröinti ei onnistunut")

# Käyttäjien hallinta
@app.route("/admin/users")
def ad_user_list():
    admin_name = admins.get_adminname()
    list = users.get_userlist()
    return render_template("adusers.html", admin_name = admin_name, userlist=list)

# Käyttäjän oikeuksien muuttaminen
@app.route("/admin/usermod/<int:user_id>")
def ad_user_mod(user_id):
    user_data = users.get_userdata(user_id)
    return render_template("adusermod.html", user_id=user_data[0], user_name=user_data[1], user_alias=user_data[2], user_rights=user_data[3])

# Käyttäjäoikeuksien muutoksen talletus tietokantaan
@app.route("/admin/usersave/<int:user_id>", methods=["post"])
def ad_user_save(user_id):
    user_rights = request.form["privileges"]
    if users.modify(user_id, user_rights):
        return redirect("/admin/users")
    else:
        return render_template("error.html",message="Muutosten talletus ei onnistunut")

def isBlank (myString):
    return not (myString and myString.strip())

