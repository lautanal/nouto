from db import db
from datetime import date, timedelta


def get_date(date_id):
    sql = "SELECT date FROM calendar WHERE id = :date_id"
    result = db.session.execute(sql, {"date_id":date_id})
    return result.fetchone()[0]

def get_today():
    today = date.today()
    sql = "SELECT id FROM calendar WHERE date = :today"
    result = db.session.execute(sql, {"today":today})
    return result.fetchone()[0]

def get_week():
    today = date.today()
    day7 = date.today() + timedelta(days=7)
    sql = "SELECT week_nr FROM calendar WHERE date > :today AND date < :day7 AND work_day = TRUE"
    result = db.session.execute(sql, {"today":today, "day7":day7})
    return result.fetchone()[0]

def get_next_week(week_nr, ndays):
    sql = "SELECT date FROM calendar WHERE week_nr = :week_nr"
    result = db.session.execute(sql, {"week_nr":week_nr})
    day7 = result.fetchone()[0] + timedelta(days=ndays)
    sql = "SELECT week_nr FROM calendar WHERE date = :day7"
    result = db.session.execute(sql, {"day7":day7})
    week_nr = result.fetchone()[0]
    return week_nr

def get_days(week_nr):
    sql = "SELECT date, id FROM calendar WHERE week_nr=:week_nr AND day_nr < 6 ORDER BY DATE"
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