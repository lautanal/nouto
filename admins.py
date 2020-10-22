from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

# Admin login
def login(username,password):
    sql = "SELECT password, id FROM admins WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    admin = result.fetchone()
    if admin == None:
        return False
    else:
        if check_password_hash(admin[0],password):
            session["admin_id"] = admin[1]
            return True
        else:
            return False

# Admin logout
def logout():
    del session["admin_id"]

# Uusi admin käyttäjä
def register(username,password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO admins (username,password) VALUES (:username,:password)"
        db.session.execute(sql, {"username":username,"password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username,password)

def admin_id():
    return session.get("admin_id",0)

def get_adminname():
    admin_id = session.get("admin_id",0)
    sql = "SELECT username FROM admins WHERE id=:admin_id"
    result = db.session.execute(sql, {"admin_id":admin_id})
    return result.fetchone()[0]
