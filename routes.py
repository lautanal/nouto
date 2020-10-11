from app import app
from flask import render_template, request, redirect, flash, Markup
from datetime import date, timedelta
import users, cal, customers, orders

varattu = [0,0,1,0,1,0,1,0,1,0,0,0,0,0,0]
hinnat = [0,0,0,0,0]
viikko_delta = 0

# Aloitus
@app.route("/")
def index():
    return render_template("index.html")

# Info
@app.route("/info")
def info():
    return render_template("info.html")

# Ajanvaraus
@app.route("/ajanvaraus", methods=["post"])
def ajanvaraus():
    global varattu, hinnat, viikko_delta

    noutolaji = request.form["noutolaji"]
    kuvaus = request.form["kuvaus"]
    postinumero = request.form["postinumero"]
    if isBlank(kuvaus) :
        return render_template("index.html", noutolaji=noutolaji, kuvaus=kuvaus, postinumero=postinumero, error="Täytä noudettavan tavaran laatu")
    if isBlank(postinumero) :
        return render_template("index.html", noutolaji=noutolaji, kuvaus=kuvaus, postinumero=postinumero, error="Täytä postinumero")
    if (len(postinumero) != 5):
        return render_template("index.html", noutolaji=noutolaji, kuvaus=kuvaus, postinumero=postinumero, error="Virheellinen postinumero")
    if (postinumero[0] != "0" or not (postinumero[1] == "0" or postinumero[1] == "1" or postinumero[1] == "2")):
        return render_template("index.html", noutolaji=noutolaji, kuvaus=kuvaus, postinumero=postinumero, error="Postinumero hakualueen ulkopuolella")

    viikko_nr = cal.get_week()
    viikko_delta = 0
    paivat = cal.get_days(viikko_nr)
    max_var = 3
    if (noutolaji == "3"):
        max_var = 2
    varaukset = orders.get_orders(viikko_nr, max_var)

    if (noutolaji == "1"):
        hinnat = [59,59,59,59,59]
    elif (noutolaji == "2"):
        hinnat = [99,99,99,99,99]
    elif(noutolaji == "3"):
        hinnat = [149,149,149,149,149]
    today_id = cal.get_today()
    for day in range(5):
        if (paivat[day][1] - today_id < 8):
            hinnat[day] += 20
        elif (paivat[day][1] - today_id < 15):
            hinnat[day] += 10

    return render_template("ajanvaraus.html", noutolaji=noutolaji, kuvaus=kuvaus, postinumero=postinumero, viikko_nr=viikko_nr, paivat=paivat, varattu=varaukset, hinnat=hinnat)

# Seuraava viikko
@app.route("/seuraava/<int:wnr>/<string:noutolaji>/<string:kuvaus>/<string:postinumero>")
def seuraavaviikko(wnr,noutolaji, kuvaus, postinumero):
    global varattu, hinnat, viikko_delta

    viikko_nr=wnr
    if (viikko_delta < 8):
        viikko_delta += 1
        viikko_nr += 1
#        viikko_nr = cal.get_next_week(wnr)

    paivat = cal.get_days(viikko_nr)
    max_var = 3
    if (noutolaji == "3"):
        max_var = 2
    varaukset = orders.get_orders(viikko_nr, max_var)

    if (noutolaji == "1"):
        hinnat = [59,59,59,59,59]
    elif (noutolaji == "2"):
        hinnat = [99,99,99,99,99]
    elif(noutolaji == "3"):
        hinnat = [149,149,149,149,149]
    today_id = cal.get_today()
    for day in range(5):
        if (paivat[day][1] - today_id < 8):
            hinnat[day] += 20
        elif (paivat[day][1] - today_id < 15):
            hinnat[day] += 10
    return render_template("ajanvaraus.html", noutolaji=noutolaji, kuvaus=kuvaus, postinumero=postinumero, viikko_nr=viikko_nr, paivat=paivat, varattu=varaukset, hinnat=hinnat)

# Edellinen viikko
@app.route("/edellinen/<int:wnr>/<string:noutolaji>/<string:kuvaus>/<string:postinumero>")
def edellinenviikko(wnr,noutolaji, kuvaus, postinumero):
    global varattu, hinnat, viikko_delta
    viikko_nr=wnr
    if (viikko_delta > 0):
        viikko_delta -= 1
        viikko_nr -= 1
#        viikko_nr = cal.get_prev_week(wnr)

    paivat = cal.get_days(viikko_nr)
    max_var = 3
    if (noutolaji == "3"):
        max_var = 2
    varaukset = orders.get_orders(viikko_nr, max_var)

    if (noutolaji == "1"):
        hinnat = [59,59,59,59,59]
    elif (noutolaji == "2"):
        hinnat = [99,99,99,99,99]
    elif(noutolaji == "3"):
        hinnat = [149,149,149,149,149]
    today_id = cal.get_today()
    for day in range(5):
        if (paivat[day][1] - today_id < 8):
            hinnat[day] += 20
        elif (paivat[day][1] - today_id < 15):
            hinnat[day] += 10
    return render_template("ajanvaraus.html", noutolaji=noutolaji, kuvaus=kuvaus, postinumero=postinumero, viikko_nr=viikko_nr, paivat=paivat, varattu=varaukset, hinnat=hinnat)

# Vahvistus
@app.route("/vahvistus/<int:wnr>", methods=["post"])
def vahvistus(wnr):
    global hinnat
    noutolaji = request.form["noutolaji"]
    kuvaus = request.form["kuvaus"]
    postinumero = request.form["postinumero"]
    tsel = request.form["aika"]
    paivat = cal.get_days(wnr)
    day_nr = int(int(tsel)/3)
    date_id = paivat[day_nr][1]
    date = cal.get_date(date_id)
    time_frame = int(tsel) - 3*day_nr + 1
    phinta = hinnat[day_nr]

    if (time_frame == 1):
         clock = "8-12"
    elif (time_frame == 2):
         clock = "12-16"
    else:
         clock = "16-19"

    return render_template("vahvistus.html", noutolaji=noutolaji, kuvaus=kuvaus, postinumero=postinumero, date_id=date_id, time_frame=time_frame, day_nr=day_nr, pvm=date, klo=clock, hinta=phinta)

# Uusi varaus tietokantaan
@app.route("/sendcust", methods=["post"])
def sendcust():
    ttype = request.form["noutolaji"]
    desc = request.form["kuvaus"]
    date_id = request.form["date_id"]
    time_frame = request.form["time_frame"]
    price = request.form["hinta"]
    name = request.form["nimi"]
    address = request.form["osoite"]
    postcode = request.form["postinumero"]
    city = request.form["kaupunki"]
    phone = request.form["puhelin"]
    email = request.form["email"]
    instructions = request.form["viesti"]

    date = cal.get_date(date_id)
    day_nr = date.isoweekday()

    if (time_frame == 1):
        clock = "8-12"
    elif (time_frame == 2):
        clock = "12-16"
    else:
        clock = "16-19"

    if (ttype == "1"):
        time_req = 1
    elif (ttype == "2"):
        time_req = 1
    elif(ttype == "3"):
        time_req = 2

    if isBlank(name) or isBlank(address) or isBlank(city) or isBlank(phone):
        return render_template("vahvistus.html", noutolaji=ttype, kuvaus=desc, postinumero=postcode, date_id=date_id, time_frame=time_frame, day_nr=day_nr, pvm=date, klo=clock, hinta=price, nimi=name, osoite=address,  kaupunki=city, puhelin=phone, email=email)
    cust_id = customers.insert(name, address, postcode, city, phone, email, instructions)
    orders.insert(cust_id, date_id, time_frame, ttype, desc, time_req, price, 0)
    date = cal.get_date(date_id)
    return render_template("valmis.html", day_nr=day_nr, pvm=date, klo=clock, noutolaji=ttype, kuvaus=desc, hinta=price, nimi=name, osoite=address, postinumero=postcode, kaupunki=city, puhelin=phone, email=email, viesti=instructions)

# Kalenterin täyttö
@app.route("/cal")
def calfill():
    cal.fill(2020, 2192)
    return redirect("/")

# Varauskalenteri
@app.route("/lista")
def worklist_today():
    d_id = cal.get_today()
    date = cal.get_date(d_id)
    day_nr = date.isoweekday()
    if (day_nr == 6):
        d_id += 2
        date = cal.get_date(d_id)
        day_nr = 1
    elif (day_nr == 7):
        d_id += 1
        date = cal.get_date(d_id)
        day_nr = 1
    tlist1 = orders.get_work_list(d_id, 1)
    tlist2 = orders.get_work_list(d_id, 2)
    tlist3 = orders.get_work_list(d_id, 3)
    return render_template("varaukset.html", date_id=d_id, pvm=date, day_nr=day_nr, tasks1=tlist1, tasks2=tlist2, tasks3=tlist3)

# Varauskalenteri
@app.route("/lista/<int:d_id>/<int:step>")
def worklist(d_id, step):
    date = cal.get_date(d_id)
    day_nr = date.isoweekday()
    if (day_nr == 6):
        if (step == 1):
            d_id -= 1
            day_nr = 5
        elif (step == 2):
            d_id += 2
            day_nr = 1
        date = cal.get_date(d_id)
    elif (day_nr == 7):
        if (step == 1):
            d_id -= 2
            day_nr = 5
        elif (step == 2):
            d_id += 1
            day_nr = 1
        date = cal.get_date(d_id)
    tlist1 = orders.get_work_list(d_id, 1)
    tlist2 = orders.get_work_list(d_id, 2)
    tlist3 = orders.get_work_list(d_id, 3)
    return render_template("varaukset.html", date_id=d_id, pvm=date, day_nr=day_nr, tasks1=tlist1, tasks2=tlist2, tasks3=tlist3)

def isBlank (myString):
    return not (myString and myString.strip())


