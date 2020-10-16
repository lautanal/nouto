from db import db
import cal

# Päivän varausten listaus
def get_work_list(date_id, time_frame):
    sql = "SELECT O.task_type, O.description, O.price, C.address, C.postcode, C.city, C.name, C.phone, C.email, C.instructions FROM orders O, customers C " \
        "WHERE O.customer_id=C.id AND O.date_id=:date_id AND O.time_frame=:time_frame"
    result = db.session.execute(sql, {"date_id":date_id, "time_frame":time_frame})
    olist=result.fetchall()
    return olist

# Viikon varausten haku
def get_orders(week_nr, max):
    varaukset = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    sql = "SELECT C.id, C.day_nr, O.time_frame, SUM(time_required) FROM calendar C, orders O " \
        "WHERE C.week_nr=:week_nr AND C.day_nr < 6 AND O.date_id=C.id GROUP BY C.id, C.day_nr, O.time_frame"
    result = db.session.execute(sql, {"week_nr":week_nr})
    olist=result.fetchall()
    today_id = cal.get_today_id()
    for ol in olist:
        iday = int(ol[1])
        itfr = int(ol[2])
        isum = int(ol[3])
        if isum > max:
            varaukset[(iday-1)*3 + itfr - 1] = 1
        if ol[0] <= today_id:
            varaukset[(iday-1)*3  + itfr -1] = 1 
# Menneet päivät  
#   pweek = cal.get_week()
#    if (week_nr == pweek):
#        wday = cal.get_today().isoweekday()
#        for day in range(wday):
#            varaukset[3*day] = 1
#            varaukset[3*day + 1] = 1
#            varaukset[3*day + 2] = 1
    return varaukset

# Uuden tilauksen talletus tietokantaan
def insert(cust_id, date_id, time_fr, ttype, desc, time_req, price, discount):
    sql = "INSERT INTO orders (customer_id, date_id, time_frame, task_type, description, time_required, price, discount) " \
        "VALUES (:cust_id, :date_id, :time_fr, :ttype, :desc, :time_req, :price, :discount)"
    db.session.execute(sql, {"cust_id":cust_id, "date_id":date_id, "time_fr":time_fr, "ttype":ttype, "desc":desc, "time_req":time_req, "price":price, "discount":discount})
    db.session.commit()
    return True
