from db import db

# Päivän tilausten haku
def get_orders(date_id):
    sql = "SELECT O.time_frame, O.time_required FROM orders O WHERE O.date_id=:date_id ORDER BY O.time_frame"
    result = db.session.execute(sql, {"date_id":date_id})
    return result.fetchall()


# Uuden tilauksen talletus tietokantaan
def insert(cust_id, date_id, time_fr, ttype, desc, time_req, price, discount):
    sql = "INSERT INTO orders (customer_id, date_id, time_frame, task_type, description, time_required, price, discount) VALUES (:cust_id, :date_id, :time_fr, :ttype, :desc, :time_req, :price, :discount)"
    db.session.execute(sql, {"cust_id":cust_id, "date_id":date_id, "time_fr":time_fr, "ttype":ttype, "desc":desc, "time_req":time_req, "price":price, "discount":discount})
    db.session.commit()
    return True
