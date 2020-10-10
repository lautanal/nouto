from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

# Login
def login(username,password):
    sql = "SELECT password, id , privileges FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    if user[2] == 0:
        return False
    else:
        if check_password_hash(user[0],password):
            session["user_id"] = user[1]
            return True
        else:
            return False

# Logout
def logout():
    del session["user_id"]

# Uusi käyttäjä
def register(username,password,alias):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password,privileges,alias) VALUES (:username,:password,1,:alias)"
        db.session.execute(sql, {"username":username,"password":hash_value,"alias":alias})
        db.session.commit()
    except:
        return False
    return login(username,password)

def login_id():
    return session.get("user_id",0)

def get_userdata(user_id):
    sql = "SELECT id, username, alias, privileges FROM users WHERE id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchone()

def get_username(user_id):
    sql = "SELECT username FROM users WHERE id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchone()[0]

# Käyttäjän alias
def get_useralias(user_id):
#    user_id = session.get("user_id",0)
    sql = "SELECT alias FROM users WHERE id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchone()[0]

# Käyttäjän oikeudet
def get_userrights(user_id):
    sql = "SELECT privileges FROM users WHERE id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchone()[0]

# Käyttäjälista
def get_userlist():
    sql = "SELECT id, username, alias, privileges FROM users ORDER BY username"
    result = db.session.execute(sql)
    return result.fetchall()

# Käyttäjätietojen muuttaminen
def modify(user_id, user_rights):
    admin_id = session.get("admin_id",0)
    if admin_id == 0:
        return False
    sql = "UPDATE users SET privileges = :user_rights WHERE id = :user_id"
    db.session.execute(sql, {"user_id":user_id,"user_rights":user_rights})
    db.session.commit()
    return True
