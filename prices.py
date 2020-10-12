from db import db
import cal

def prices(day_id, noutolaji):
    if (noutolaji == "1"):
        hinnat = [59,59,59,59,59]
    elif (noutolaji == "2"):
        hinnat = [99,99,99,99,99]
    elif(noutolaji == "3"):
        hinnat = [149,149,149,149,149]
    today_id = cal.get_today_id()
    for day in range(5):
        if (day_id - today_id < 8):
            hinnat[day] += 20
        elif (day_id - today_id < 15):
            hinnat[day] += 10
        day_id += 1
    return hinnat