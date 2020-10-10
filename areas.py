from db import db
from datetime import date, timedelta

# Keskustelualueiden haku (käyttöoikeuksien mukaan)
def fill(year):
    day = date(year,1,1)
    week_nr = 1
    for dnr in range(365):
        day_nr = day.isoweekday()
        if (day_nr == 1):
            week_nr = week_nr + 1
        if (day_nr < 6):
             work_day = True
        else:
            work_day = False
        sql = "INSERT INTO calendar (date, week_nr, day_nr, work_day) VALUES (:date, :week_nr, :day_nr, :work_day)"
        db.session.execute(sql, {"date":day, "week_nr":week_nr,  "day_nr":day_nr,  "work_day":work_day})
        db.session.commit()
        day = day + timedelta(days=1)
    return True

