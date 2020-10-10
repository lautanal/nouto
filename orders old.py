from db import db


# Päivän tilausten haku
def get_orders(topic_id):
    sql = "SELECT O.time_frame, O.time_required FROM orders O WHERE O.date_id=:date_id ORDER BY O.time_frame"
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchall()

# Viestien haku tietojen perusteella
def find_messages(user_alias, content):
    user_alias = "%" + user_alias + "%"
    content = "%" + content + "%"
    if (user_alias == ""):
        sql = "SELECT M.id, M.content, U.id, U.alias, M.sent_at, M.ref_message FROM messages M, users U WHERE M.visible = true AND M.user_id=U.id AND M.content LIKE :content ORDER BY M.id"
        result = db.session.execute(sql, {"content":content})
    elif(content == ""):
        sql = "SELECT M.id, M.content, U.id, U.alias, M.sent_at, M.ref_message FROM messages M, users U WHERE M.visible = true AND M.user_id=U.id AND U.alias LIKE :user_alias ORDER BY M.id"
        result = db.session.execute(sql, {"user_alias":user_alias})
    else:
        sql = "SELECT M.id, M.content, U.id, U.alias, M.sent_at, M.ref_message FROM messages M, users U WHERE M.visible = true AND M.user_id=U.id AND U.alias LIKE :user_alias AND M.content LIKE :content  ORDER BY M.id"
        result = db.session.execute(sql, {"user_alias":user_alias, "content":content})
    return result.fetchall()

# Uuden tilauksen talletus tietokantaan
def insert(customer_id, date_id, time_frame, task_type, description, time_required, price, discount):
#    login_id = users.login_id()
#    if login_id == 0:
#       return False
    sql = "INSERT INTO orders (customer_id, date_id, time_frame, type_of_work, description, time_required, price, discount, notes) VALUES (:cust_id, :date_id, :time_fr, :wtype, :desc, :time_req, :price, :discount, :notes)"
    db.session.execute(sql, {"cust_id":cust_id, "date_id":date_id, "time_fr":time_fr, "wtype":wtype, "desc":desc, "time_req":time_req, "price":price, "discount":discount, "notes":notes})
    db.session.commit()
    return True

# Viestin poistaminen (näkyviltä)
def delete(message_id):
    login_id = users.login_id()
    if login_id == 0:
        return False
    sql = "UPDATE messages SET visible = false WHERE id = :message_id"
#    sql = "DELETE FROM messages WHERE id=:message_id"
    db.session.execute(sql, {"message_id":message_id})
    db.session.commit()
    return True

# Muutetun viestin talletus tietokantaan
def update(message_id, content):
    login_id = users.login_id()
    if login_id == 0:
        return False
    sql = "UPDATE messages SET CONTENT = :content WHERE id = :message_id"
    db.session.execute(sql, {"content":content, "message_id":message_id})
    db.session.commit()
    return True

# Viestin poistaminen (administraattori)
def admin_delete(message_id):
    admin_id = admins.admin_id()
    if admin_id == 0:
        return False
    sql = "UPDATE messages SET visible = false WHERE id = :message_id"
    db.session.execute(sql, {"message_id":message_id})
    db.session.commit()
    return True

