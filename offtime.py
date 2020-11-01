from db import db
import cal

# Vapaa-aikojen haku
def get_offtime(week_nr):
    offtime = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    sql = "SELECT C.day_nr, O.p1, O.p2, O.p3, O.p4 FROM calendar C, offtimes O WHERE C.week_nr=:week_nr AND C.day_nr < 6 AND O.date_id=C.id"
    result = db.session.execute(sql, {"week_nr":week_nr})
    olist=result.fetchall()
    for ol in olist:
        iday = int(ol[0])
        p1 = int(ol[1])
        p2 = int(ol[2])
        p3 = int(ol[3])
        p4 = int(ol[4])
        if p1 != 0:
            offtime[(iday-1)*4] = 1
        if p2 != 0:
            offtime[(iday-1)*4 + 1] = 1
        if p3 != 0:
            offtime[(iday-1)*4 + 2] = 1
        if p4 != 0:
            offtime[(iday-1)*4 + 3] = 1
    return offtime

# Vapaa-aikojen talletus tietokantaan
def update(week_nr, day_id, offlist):
# Vanhojen vapaiden haku tietokannasta
    old_off = get_offtime(week_nr)
# Uuden vapaan talletus tai update
    for day in range(5):
        old_check = old_off[day*4]+old_off[day*4+1]+old_off[day*4+2]+old_off[day*4+3]
        new_check = offlist[day*4]+offlist[day*4+1]+offlist[day*4+2]+offlist[day*4+3]
        if old_check == 0 and new_check != 0:
            sql = "INSERT INTO offtimes (date_id,p1,p2,p3,p4) VALUES (:day_id,:p1,:p2,:p3,:p4)"
            db.session.execute(sql, {"day_id":day_id, "p1":offlist[day*4], "p2":offlist[day*4+1],"p3":offlist[day*4+2],"p4":offlist[day*4+3]})
            db.session.commit()
        elif old_check != 0 and new_check == 0:
            sql = "DELETE FROM offtimes WHERE date_id=:day_id"
            db.session.execute(sql, {"day_id":day_id})
            db.session.commit()
        elif old_check != 0 and new_check != 0:
            if offlist[day*4] != old_off[day*4] or offlist[day*4+1] != old_off[day*4+1] or offlist[day*4+2] != old_off[day*4+2] or offlist[day*4+3] != old_off[day*4+3]:
                sql = "UPDATE offtimes SET p1=:p1, p2=:p2, p3=:p3, p4=:p4 WHERE date_id=:day_id"
                db.session.execute(sql, {"day_id":day_id, "p1":offlist[day*4], "p2":offlist[day*4+1],"p3":offlist[day*4+2],"p4":offlist[day*4+3]})
                db.session.commit()
        day_id += 1
    return True

