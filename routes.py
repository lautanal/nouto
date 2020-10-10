from app import app
from flask import render_template, request, redirect, flash, Markup
from datetime import date, timedelta
import users, cal, customers, orders

varattu = [0,0,1,0,1,0,1,0,1,0,0,0,0,0,0]
hinta = [59,59,59,59,59]
viikko_nr = 0
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
    global varattu, hinta, viikko_nr, viikko_delta
    noutolaji = request.form["noutolaji"]
    kuvaus = request.form["kuvaus"]
    postinumero = request.form["postinumero"]
    if isBlank(kuvaus) or isBlank(postinumero) :
        return redirect("/")
    viikko_nr = cal.get_week()
    viikko_delta = 0
    paivat = cal.get_days(viikko_nr)
    if (noutolaji == "1"):
        hinta = [59,59,59,59,59]
    elif (noutolaji == "2"):
        hinta = [99,99,99,99,99]
    elif(noutolaji == "3"):
        hinta = [149,149,149,149,149]
    today_id = cal.get_today()
    for day in range(5):
        if (paivat[0][1] - today_id < 8):
            hinta[day] += 20
        elif (paivat[0][1] - today_id < 15):
            hinta[day] += 10

    return render_template("ajanvaraus.html", noutolaji=noutolaji, kuvaus=kuvaus, postinumero=postinumero, viikko_nr=viikko_nr % 100, paivat=paivat, varattu=varattu, hinta=hinta)

# Viikon vaihto
@app.route("/viikko/<int:muutos>/<string:noutolaji>/<string:postinumero>/<string:kuvaus>")
def viikko(muutos, noutolaji, postinumero, kuvaus):
    global varattu, hinta, viikko_nr, viikko_delta
    if (muutos == 1):
        if (viikko_delta > 0):
            viikko_delta -= 1
            viikko_nr = cal.get_next_week(viikko_nr, -7)
    else:
        if (viikko_delta < 8):
            viikko_delta += 1
            viikko_nr = cal.get_next_week(viikko_nr, 7)
    paivat = cal.get_days(viikko_nr)
    if (noutolaji == "1"):
        hinta = [59,59,59,59,59]
    elif (noutolaji == "2"):
        hinta = [99,99,99,99,99]
    elif(noutolaji == "3"):
        hinta = [149,149,149,149,149]
    today_id = cal.get_today()
    for day in range(5):
        if (paivat[0][1] - today_id < 8):
            hinta[day] += 20
        elif (paivat[0][1] - today_id < 15):
            hinta[day] += 10
    return render_template("ajanvaraus.html", noutolaji=noutolaji, kuvaus=kuvaus, postinumero=postinumero, viikko_nr=viikko_nr % 100, paivat=paivat, varattu=varattu, hinta=hinta)

# Vahvistus
@app.route("/vahvistus", methods=["post"])
def vahvistus():
    global hinta
    noutolaji = request.form["noutolaji"]
    kuvaus = request.form["kuvaus"]
    postinumero = request.form["postinumero"]
    tsel = request.form["aika"]
    paivat = cal.get_days(viikko_nr)
    daynr = int(int(tsel)/3)
    date_id = paivat[daynr][1]
    date = cal.get_date(date_id)
    time_frame = int(tsel) - 3*daynr + 1
    phinta = hinta[daynr]

    if (time_frame == 1):
         clock = "8-12"
    elif (time_frame == 2):
         clock = "12-16"
    else:
         clock = "16-19"

    if (daynr == 0):
        viikonpv = "maanantai"
    elif (daynr == 1):
        viikonpv = "tiistai"
    elif (daynr == 2):
        viikonpv = "keskiviikko"
    elif (daynr == 3):
        viikonpv = "torstai"
    elif (daynr == 4):
        viikonpv = "perjanta"

    return render_template("vahvistus.html", noutolaji=noutolaji, kuvaus=kuvaus, postinumero=postinumero, date_id=date_id, time_frame=time_frame, viikonpv=viikonpv, pvm=date, klo=clock, hinta=phinta)

# Uusi varaus tietokantaan
@app.route("/sendcust", methods=["post"])
def sendcust():
    global hinta
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
    if (day_nr == 1):
        viikonpv = "maanantai"
    elif (day_nr == 2):
        viikonpv = "tiistai"
    elif (day_nr == 3):
        viikonpv = "keskiviikko"
    elif (day_nr == 4):
        viikonpv = "torstai"
    elif (day_nr == 5):
        viikonpv = "perjantai"

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
        return render_template("vahvistus.html", noutolaji=ttype, kuvaus=desc, postinumero=postcode, date_id=date_id, time_frame=time_frame, viikonpv=viikonpv, pvm=date, klo=clock, hinta=price, nimi=name, osoite=address,  kaupunki=city, puhelin=phone, email=email)
    cust_id = customers.insert(name, address, postcode, city, phone, email, instructions)
    orders.insert(cust_id, date_id, time_frame, ttype, desc, time_req, price, 0)
    date = cal.get_date(date_id)
    return render_template("valmis.html", viikonpv=viikonpv, pvm=date, klo=clock, noutolaji=ttype, kuvaus=desc, hinta=price, nimi=name, osoite=address, postinumero=postcode, kaupunki=city, puhelin=phone, email=email, viesti=instructions)

# Kalenterin täyttö
@app.route("/cal")
def calfill():
    cal.fill(2020, 2192)
    return redirect("/")

def isBlank (myString):
    return not (myString and myString.strip())


