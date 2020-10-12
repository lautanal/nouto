from db import db
from datetime import date, timedelta


def get_date(date_id):
    sql = "SELECT date FROM calendar WHERE id = :date_id"
    result = db.session.execute(sql, {"date_id":date_id})
    return result.fetchone()[0]

def get_today_id():
    today = date.today()
    sql = "SELECT id FROM calendar WHERE date = :today"
    result = db.session.execute(sql, {"today":today})
    return result.fetchone()[0]

def get_today():
    today = date.today()
    sql = "SELECT date FROM calendar WHERE date = :today"
    result = db.session.execute(sql, {"today":today})
    return result.fetchone()[0]

def get_week():
    today = date.today()
    sql = "SELECT week_nr FROM calendar WHERE date > :today AND work_day = TRUE ORDER BY id LIMIT 5"
    result = db.session.execute(sql, {"today":today})
    return result.fetchone()[0]

def get_next_week(week_nr):
    print("NEXT WEEK: ", week_nr)
    sql = "SELECT week_nr FROM calendar WHERE week_nr > :week_nr ORDER BY id LIMIT 1"
    result = db.session.execute(sql, {"week_nr":week_nr})
    return result.fetchone()[0]

#    day7 = result.fetchone()[0]
#    day7 = day7 + timedelta(days=ndays)
#    sql = "SELECT week_nr FROM calendar WHERE date = :day7"
#    result = db.session.execute(sql, {"day7":day7})

def get_prev_week(week_nr):
    print("PREV WEEK: ", week_nr)
    sql = "SELECT id FROM calendar WHERE week_nr = :week_nr LIMIT 1"
    result = db.session.execute(sql, {"week_nr":week_nr})
    day_id = result.fetchone()[0]
    day_id -= 7
    sql = "SELECT week_nr FROM calendar WHERE id = :day_id"
    result = db.session.execute(sql, {"day_id":day_id})
    return result.fetchone()[0]

def get_days(week_nr):
    sql = "SELECT date, id FROM calendar WHERE week_nr=:week_nr AND day_nr < 6 ORDER BY id"
    result = db.session.execute(sql, {"week_nr":week_nr})
    return result.fetchall()

def fill(year, days):
    day = date(year,1,1)
    week_nr = day.isocalendar()[1] + (day.year-2000)*100
    for dnr in range(days):
        day_nr = day.isoweekday()
        if (day_nr == 1):
            week_nr = day.isocalendar()[1] + (day.year-2000)*100
        if (day_nr < 6):
             work_day = True
        else:
            work_day = False
        sql = "INSERT INTO calendar (date, week_nr, day_nr, work_day) VALUES (:date, :week_nr, :day_nr, :work_day)"
        db.session.execute(sql, {"date":day, "week_nr":week_nr,  "day_nr":day_nr,  "work_day":work_day})
        db.session.commit()
        day = day + timedelta(days=1)
    return True