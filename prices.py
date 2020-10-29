from db import db
import cal

# Hintojen määrittely
def prices(week_nr, day_id, noutolaji, city, p_extra):
    if (noutolaji == "1"):
        hinnat = [79,59,59,79,79,59,59,79,79,59,59,79,79,59,59,79,79,59,59,79]
        alin_hinta = 59
    elif (noutolaji == "2"):
        hinnat = [119,99,99,119,119,99,99,119,119,99,99,119,119,99,99,119,119,99,99,119]
        alin_hinta = 99
    elif(noutolaji == "3"):
        hinnat = [169,149,149,169,169,149,149,169,169,149,149,169,169,149,149,169,169,149,149,169]
        alin_hinta = 149
    for i in range(20):
        hinnat[i] = hinnat[i] + p_extra

# Päivän lisähinta tai alennus
    sql = "SELECT C.day_nr, P.p1 FROM calendar C, prices P WHERE C.week_nr=:week_nr AND C.day_nr < 6 AND P.date_id=C.id"
    result = db.session.execute(sql, {"week_nr":week_nr})
    olist=result.fetchall()
#    print("WEEK: ", week_nr)
#    print("OLIST: ", olist)
    for ol in olist:
        iday = int(ol[0])
        p1 = int(ol[1])
        hinnat[(iday-1)*4] += p1 
        hinnat[(iday-1)*4 + 1] += p1 
        hinnat[(iday-1)*4 + 2] += p1 
        hinnat[(iday-1)*4 + 3] += p1 

# Lisämaksu jos varaus alle viikon päässä
    today_id = cal.get_today_id()
    for day in range(5):
        if (day_id - today_id < 8):
            hinnat[day*4] += 10
            hinnat[day*4+1] += 10
            hinnat[day*4+2] += 10
            hinnat[day*4+3] += 10
        day_id += 1

# Kympin alennus jos muita noutoja samalta alueella samassa slotissa
    sql = "SELECT DISTINCT C.id, C.day_nr, O.time_frame from calendar C, orders O, customers U " \
        "WHERE C.week_nr=:week_nr AND O.date_id=C.id AND O.customer_id=U.id AND U.city=:city AND O.deleted IS NULL " \
        "ORDER BY C.day_nr, O.time_frame"
    result = db.session.execute(sql, {"week_nr":week_nr, "city":city})
    olist=result.fetchall()
    for ol in olist:
        d_id = ol[0]
        iday = int(ol[1])
        itfr = int(ol[2])
        if hinnat[(iday-1)*4 + itfr -1] > alin_hinta:
            hinnat[(iday-1)*4 + itfr -1] -= 10 

    return hinnat

# Valitun päivän hinta
def get_price(day_id, time_frame, noutolaji, city, p_extra):
    if (noutolaji == "1"):
        price = 59
        lowest_price = 59;
    elif (noutolaji == "2"):
        price = 99
        lowest_price = 99;
    elif(noutolaji == "3"):
        price = 149
        lowest_price = 149;
    price = price + p_extra
    today_id = cal.get_today_id()
    if time_frame == 1 or time_frame == 4:
        price += 20

# Päivän lisähinta tai alennus
    sql = "SELECT p1 FROM prices WHERE date_id=:day_id"
    result = db.session.execute(sql, {"day_id":day_id})
    add=result.fetchone()
    if add:
        price += add[0]

# Lisämaksu jos tilaus alle viikon päässä
    if (day_id - today_id < 8):
        price += 10

# Alennus jos muita noutoja samalta alueella samassa slotissa
        sql = "SELECT DISTINCT O.date_id, O.time_frame from orders O, customers U " \
            "WHERE O.date_id=:day_id AND O.time_frame=:time_frame AND O.customer_id=U.id AND U.city=:city AND O.deleted IS NULL "
        result = db.session.execute(sql, {"day_id":day_id, "time_frame":time_frame, "city":city})
        if result.fetchone() and price > lowest_price:
            price -= 10

    return price

# Lisähintojen ja alennusten haku
def get_add_prices(week_nr):
    add_prices = [0,0,0,0,0]
    sql = "SELECT C.day_nr, P.p1 FROM calendar C, prices P WHERE C.week_nr=:week_nr AND C.day_nr < 6 AND P.date_id=C.id"
    result = db.session.execute(sql, {"week_nr":week_nr})
    olist=result.fetchall()

    for ol in olist:
        iday = int(ol[0])
        p1 = int(ol[1])
        add_prices[iday-1] = p1

    return add_prices

# Uusien hintojen talletus tietokantaan
def update(week_nr, day_id, new_prices):
# Vanhojen hintojen haku tietokannasta
    old_prices = [-999,-999,-999,-999,-999]
    sql = "SELECT C.day_nr, P.p1 FROM calendar C, prices P WHERE C.week_nr=:week_nr AND C.day_nr < 6 AND P.date_id=C.id"
    result = db.session.execute(sql, {"week_nr":week_nr})
    olist=result.fetchall()
    for ol in olist:
        iday = int(ol[0])
        p1 = int(ol[1])
        old_prices[iday-1] = p1

#Uuden hinnat talletus tai update
    for day in range(5):
        if old_prices[day] == -999 and new_prices[day] != 0:
            sql = "INSERT INTO prices (date_id,p1,p2,p3,p4) VALUES (:day_id,:p1,0,0,0)"
            db.session.execute(sql, {"day_id":day_id, "p1":new_prices[day]})
            db.session.commit()
        elif old_prices[day] != -999 and new_prices[day] != old_prices[day]:
            sql = "UPDATE prices SET p1=:p1 WHERE date_id=:day_id"
            db.session.execute(sql, {"day_id":day_id, "p1":new_prices[day]})
            db.session.commit()
        day_id += 1
    return True

