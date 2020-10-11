from db import db

# Päivän tilausten haku
def get_orders(week_nr, max):
    varaukset = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    sql = "SELECT C.day_nr, O.time_frame, SUM(time_required) FROM calendar C, orders O WHERE C.week_nr=:week_nr AND C.day_nr < 6 AND O.date_id=C.id GROUP BY C.day_nr, O.time_frame"
    result = db.session.execute(sql, {"week_nr":week_nr})
    olist=result.fetchall()
    for ol in olist:
        iday = int(ol[0])
        itfr = int(ol[1])
        isum = int(ol[2])
        if (isum > max):
            varaukset[(iday-1)*3 + itfr - 1] = 1
 #       print("IDAY: ", iday)
 #       print("ITFR: ", itfr)
 #       print("ISUM: ", isum)
    return varaukset


# Uuden tilauksen talletus tietokantaan
def insert(cust_id, date_id, time_fr, ttype, desc, time_req, price, discount):
    sql = "INSERT INTO orders (customer_id, date_id, time_frame, task_type, description, time_required, price, discount) VALUES (:cust_id, :date_id, :time_fr, :ttype, :desc, :time_req, :price, :discount)"
    db.session.execute(sql, {"cust_id":cust_id, "date_id":date_id, "time_fr":time_fr, "ttype":ttype, "desc":desc, "time_req":time_req, "price":price, "discount":discount})
    db.session.commit()
    return True
