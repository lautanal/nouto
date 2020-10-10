from app import app
from flask import render_template, request, redirect, flash, Markup
from datetime import date, timedelta
import users, cal, customers, orders

varattu = [0,0,1,0,1,0,1,0,1,0,0,0,0,0,0]
hinta = [59,59,99,59,59,99,59,59,99,59,59,99,59,59,99]
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


# Noudon varaus
@app.route("/ajanvaraus", methods=["post"])
def ajanvaraus():
    global varattu, hinta, viikko_nr, viikko_delta
    noutolaji = request.form["noutolaji"]
    if (noutolaji == "1"):
        hinta = [59,59,69,59,59,69,59,59,69,59,59,69,59,59,69]
    elif (noutolaji == "2"):
        hinta = [99,99,109,99,99,109,99,99,109,99,99,109,99,99,109]
    elif(noutolaji == "3"):
        hinta = [149,149,149,149,149,149,149,149,149,149,149,149,149,149,149]
    elif (noutolaji == "4"):
        hinta = [399,399,449,399,399,449,399,399,449,399,399,449,399,399,449]
    kuvaus = request.form["kuvaus"]
    postinumero = request.form["postinumero"]
    viikko_nr = cal.get_week()
    viikko_delta = 0
    paivat = cal.get_days(viikko_nr)
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
        if (viikko_delta < 4):
            viikko_delta += 1
            viikko_nr = cal.get_next_week(viikko_nr, 7)
    paivat = cal.get_days(viikko_nr)
    return render_template("ajanvaraus.html", noutolaji=noutolaji, kuvaus=kuvaus, postinumero=postinumero, viikko_nr=viikko_nr % 100, paivat=paivat, varattu=varattu, hinta=hinta)

# Kalenterin täyttö
@app.route("/cal")
def calfill():
    cal.fill(2020, 2192)
    return redirect("/")

# Uusi varaus tietokantaan
@app.route("/sendcust", methods=["post"])
def sendcust():
    global hinta
    ttype = request.form["noutolaji"]
    desc = request.form["kuvaus"]
    tsel = request.form["aika"]
    name = request.form["nimi"]
    address = request.form["osoite"]
    postcode = request.form["postinumero"]
    city = request.form["kaupunki"]
    phone = request.form["puhelin"]
    email = request.form["email"]
    instructions = request.form["viesti"]
#    print("Tehtävän tyyppi: ", ttype)
#    print("Kuvaus: ", desc)
#   print("Aika: ", tsel)
#    print("Nimi: ", name)
#    print("osoite: ", address)
#    print("postinumero: ", postcode)
#    print("kaupunki: ", city)
#    print("puhelin: ", phone)
#    print("email: ", email)
#    print("viesti: ", instructions)
    cust_id = customers.insert(name, address, postcode, city, phone, email, instructions)
    paivat = cal.get_days(viikko_nr)
    daynr = int(int(tsel)/3)
    date_id = paivat[daynr][1]
    time_fr = int(tsel) - 3*daynr + 1
    if (ttype == "1"):
        treq = 40
    elif (ttype == "2"):
        treq = 50
    elif(ttype == "3"):
        treq = 60
    elif (ttype == "4"):
        treq = 120
    price = hinta[int(tsel)]
    orders.insert(cust_id, date_id, time_fr, ttype, desc, treq, price, 0)
    date = cal.get_date(date_id)
    if (time_fr == 1):
         clock = "8-12"
    elif (time_fr == 2):
         clock = "12-16"
    else:
         clock = "16-19"
    return render_template("confirm.html", pvm=date, klo=clock, noutolaji=ttype, kuvaus=desc, hinta=price, nimi=name, osoite=address, postinumero=postcode, kaupunki=city)
