from db import db

# Uuden tilaajan talletus tietokantaan
def insert(name, address, postcode, city, phone, email, instructions):
    sql = "INSERT INTO customers (name, address, city, postcode, phone, email, instructions) VALUES (:name, :address, :city, :postcode, :phone, :email, :instructions)"
    result = db.session.execute(sql, {"name":name, "address":address, "city":city, "postcode":postcode, "phone":phone, "email":email, "instructions":instructions})
 #   result = db.session.flush()
    sql = "SELECT MAX(id) FROM customers"
    result = db.session.execute(sql)
    cust_id = result.fetchone()[0]
    db.session.commit()
    return cust_id
