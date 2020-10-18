from db import db
import cal

def prices(day_id, noutolaji, p_extra):
    if (noutolaji == "1"):
        hinnat = [59,59,59,59,59,59,59,59,59,59,59,59,59,59,59]
    elif (noutolaji == "2"):
        hinnat = [99,99,99,99,99,99,99,99,99,99,99,99,99,99,99]
    elif(noutolaji == "3"):
        hinnat = [149,149,149,149,149,149,149,149,149,149,149,149,149,149,149]
    for i in range(15):
        hinnat[i] = hinnat[i] + p_extra

    today_id = cal.get_today_id()
    for day in range(5):
        if (day_id - today_id < 8):
            hinnat[day*3] += 10
            hinnat[day*3+1] += 10
            hinnat[day*3+2] += 10
        day_id += 1
    return hinnat

def wprices(week_nr, noutolaji):
    if (noutolaji == "1"):
        hinnat = [59,59,59,59,59,59,59,59,59,59,59,59,59,59,59]
    elif (noutolaji == "2"):
        hinnat = [99,99,99,99,99,99,99,99,99,99,99,99,99,99,99]
    elif(noutolaji == "3"):
        hinnat = [149,149,149,149,149,149,149,149,149,149,149,149,149,149,149]

    sql = "SELECT C.day_nr, P.p1, P.p2, P.p3 FROM calendar C, prices P WHERE C.week_nr=:week_nr AND C.day_nr < 6 AND P.date_id=C.id"
    result = db.session.execute(sql, {"week_nr":week_nr})
    olist=result.fetchall()

    for ol in olist:
        iday = int(ol[0])
        p1 = int(ol[1])
        p2 = int(ol[2])
        p3 = int(ol[3])
        hinnat[(iday-1)*3] += p1 
        hinnat[(iday-1)*3 + 1] += p2 
        hinnat[(iday-1)*3 + 2] += p3 

    return hinnat

def get_price(day_id, noutolaji, p_extra):
    if (noutolaji == "1"):
        price = 59
    elif (noutolaji == "2"):
        price = 99
    elif(noutolaji == "3"):
        price = 149
    price = price + p_extra
    today_id = cal.get_today_id()
    if (day_id - today_id < 8):
        price += 10
    return price