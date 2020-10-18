from app import app
from flask import render_template, request, redirect, flash, Markup
from datetime import date, timedelta
import users, cal, customers, orders, prices


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
    postinumerot = {
        "01150": "Söderkulla", "01180": "Kalkkiranta", "01190": "Box", "04130": "Sipoo",
        "01800": "Klaukkala", "01810": "Luhtajoki", "01820": "Klaukkala", "01830": "Lepsämä", "01840": "Klaukkala", "01860": "Perttula", "01900": "Nurmijärvi", "01940": "Palojoki",  
        "02390": "Sarvvik", "02400": "Kirkkonummi", "02410": "Kirkkonummi", "02420": "Jorvas", "02430": "Masala", "02440": "Luoma",   
        "02450": "Sundsberg", "02460": "Kantvik", "02470": "Upinniemi", "02480": "Kirkkonummi-Porkkala", "02490": "Pikkala",  
        "02510": "Oitmäki", "02520": "Lapinkylä", "02540": "Kylmälä", "02550": "Evitskog", "02880": "Veikkola",  
        "03100": "Nummela", "03150": "Huhmari", "03220": "Tervalampi", "03250": "Ojakkala", "03300": "Otalampi",  
        "03320": "Selki", "03400": "Vihti", "03430": "Jokikunta", "03790": "Vihtijärvi",
        "04150": "Martinkylä", "04170": "Paippinen", "04240": "Talma",   
        "04200": "Kerava", "04220": "Kerava", "04230": "Kerava", "04250": "Kerava", "04260": "Kerava-Savio", 
        "04400": "Järvenpää", "04410": "Järvenpää", "04420": "Järvenpää", "04440": "Järvenpää", "04460": "Nummenkylä", "04480": "Haarajoki"
    }

    noutolaji = request.form["noutolaji"]
    kuvaus = request.form["kuvaus"]
    postinumero = request.form["postinumero"]
    if isBlank(kuvaus) :
        return render_template("index.html", noutolaji=noutolaji, kuvaus=kuvaus, postinumero=postinumero, error="Täytä noudettavan tavaran laatu")
    if isBlank(postinumero) :
        return render_template("index.html", noutolaji=noutolaji, kuvaus=kuvaus, postinumero=postinumero, error="Täytä postinumero")
    if (len(postinumero) != 5):
        return render_template("index.html", noutolaji=noutolaji, kuvaus=kuvaus, postinumero=postinumero, error="Virheellinen postinumero")

    postin = int(postinumero)
    p_accepted = False
    p_extra = 0
    if postin < 1000:
        p_accepted = True
        kaupunki = "Helsinki"
    elif postin >= 1200 and postin <= 1770:
        p_accepted = True
        kaupunki = "Vantaa"
    elif (postin >= 2100 and postin <= 2380) or (postin >= 2600 and postin <= 2860) or (postin >= 2920 and postin <= 2980):
        p_accepted = True
        kaupunki = "Espoo"

    elif postinumero in postinumerot:
        p_accepted = True
        kaupunki = postinumerot.get(postinumero)
        p_extra = 20
    
#    (postin >= 1150 and postin <= 1190) or (postin >= 4130 and postin <= 4240):
#        p_accepted = True
#        kaupunki = "Sipoo"
#        p_extra = 20
#    elif postin >= 1800 and postin <= 1940:
#        p_accepted = True
#        kaupunki = "Nurmijärvi"
#        p_extra = 20
#    elif (postin >= 2390 and postin <= 2550) or postin == 2880:
#        p_accepted = True
#        kaupunki = "Kirkkonummi"
#        p_extra = 20
#    elif (postin >= 3100 and postin <= 3430) or postin == 3790:
#        p_accepted = True
#        kaupunki = "Vihti"
#        p_extra = 20
#    elif postin >= 4200 and postin <= 4260:
#        p_accepted = True
#        kaupunki = "Kerava"
#        p_extra = 20
#    elif postin >= 4300 and postin <= 4380:
#        p_accepted = True
#        kaupunki = "Tuusula"
#        p_extra = 20
#    elif postin >= 4400 and postin <= 4480:
#        p_accepted = True
#        if postin == 4460:
#            kaupunki = "Nummenkylä"
#        elif postin == 4480:
#            kaupunki = "Haarajoki"
#        else:
#            kaupunki = "Järvenpää"
#        p_extra = 20

    if postin == 2700:
        kaupunki = "Kauniainen" 

    if not p_accepted:
        return render_template("index.html", noutolaji=noutolaji, kuvaus=kuvaus, postinumero=postinumero, error="Postinumero hakualueen ulkopuolella")
    viikko_nr = cal.get_week()
    paivat = cal.get_days(viikko_nr)
    max_var = 3
    if noutolaji == "3":
        max_var = 2
    varaukset = orders.check_orders(viikko_nr, max_var)
    check = 14
    for slot in range(15):
        if (varaukset[14-slot] == 0):
            check = 14 - slot

    hinnat = prices.prices(paivat[0][1], noutolaji, p_extra)

    return render_template("ajanvaraus.html", noutolaji=noutolaji, kuvaus=kuvaus, postinumero=postinumero, kaupunki=kaupunki, viikko_nr=viikko_nr, vdelta=0, paivat=paivat, varattu=varaukset, hinnat=hinnat, valinta=check, p_extra=p_extra)

# Seuraava viikko
@app.route("/seuraava/<int:wnr>/<int:vdelta>/<string:noutolaji>/<string:kuvaus>/<string:postinumero>/<string:kaupunki>/<int:p_extra>")
def seuraavaviikko(wnr, vdelta, noutolaji, kuvaus, postinumero, kaupunki, p_extra):
    viikko_nr=int(wnr)
    if (vdelta < 12):
        vdelta += 1
        if (viikko_nr % 100 < 52):
            viikko_nr += 1
        else:
            viikko_nr = cal.get_next_week(viikko_nr)

    paivat = cal.get_days(viikko_nr)
    max_var = 3
    if noutolaji == "3":
        max_var = 2
    varaukset = orders.check_orders(viikko_nr, max_var)
    check = 14
    for slot in range(15):
        if (varaukset[14-slot] == 0):
            check = 14 - slot

    hinnat = prices.prices(paivat[0][1], noutolaji, int(p_extra))

    return render_template("ajanvaraus.html", noutolaji=noutolaji, kuvaus=kuvaus, postinumero=postinumero, kaupunki=kaupunki, viikko_nr=viikko_nr, vdelta=vdelta, paivat=paivat, varattu=varaukset, hinnat=hinnat, valinta=check, p_extra=p_extra)

# Edellinen viikko
@app.route("/edellinen/<int:wnr>/<int:vdelta>//<string:noutolaji>/<string:kuvaus>/<string:postinumero>/<string:kaupunki>/<int:p_extra>")
def edellinenviikko(wnr, vdelta, noutolaji, kuvaus, postinumero, kaupunki, p_extra):
    viikko_nr=int(wnr)
    if vdelta > 0:
        vdelta -= 1
        if (viikko_nr % 100 > 1):
            viikko_nr -= 1
        else:
            viikko_nr = cal.get_prev_week(viikko_nr)

    paivat = cal.get_days(viikko_nr)
    max_var = 3
    if noutolaji == "3":
        max_var = 2
    varaukset = orders.check_orders(viikko_nr, max_var)
    check = 14
    for slot in range(15):
        if (varaukset[14-slot] == 0):
            check = 14 - slot

    hinnat = prices.prices(paivat[0][1], noutolaji, int(p_extra))

    return render_template("ajanvaraus.html", noutolaji=noutolaji, kuvaus=kuvaus, postinumero=postinumero, kaupunki=kaupunki, viikko_nr=viikko_nr, vdelta=vdelta, paivat=paivat, varattu=varaukset, hinnat=hinnat, valinta=check, p_extra=p_extra)

# Vahvistus
@app.route("/vahvistus/<int:wnr>", methods=["post"])
def vahvistus(wnr):
    noutolaji = request.form["noutolaji"]
    kuvaus = request.form["kuvaus"]
    postinumero = request.form["postinumero"]
    kaupunki = request.form["kaupunki"]
    p_extra = request.form["p_extra"]

    tsel = request.form["aika"]
    paivat = cal.get_days(wnr)
    day_nr = int(tsel)//3
    date_id = paivat[day_nr][1]
    date = cal.get_date(date_id)
    time_frame = int(tsel) - 3*day_nr + 1
    phinta = prices.get_price(date_id, noutolaji, int(p_extra))
    day_nr += 1

    return render_template("vahvistus.html", noutolaji=noutolaji, kuvaus=kuvaus, postinumero=postinumero, kaupunki=kaupunki, date_id=date_id, time_frame=time_frame, day_nr=day_nr, pvm=date, hinta=phinta)

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
    accepted = False
    if request.form.get("ehdot"):
        accepted = True

    date = cal.get_date(date_id)
    day_nr = date.isoweekday()

    if ttype == "1":
        time_req = 1
    elif ttype == "2":
        time_req = 1
    elif ttype == "3":
        time_req = 2

    error = False
    if isBlank(name) or isBlank(address) or isBlank(phone):
        error = True
        error_message = "Täytä puuttuvat tiedot"
        return render_template("vahvistus.html", noutolaji=ttype, kuvaus=desc, postinumero=postcode, date_id=date_id, day_nr=day_nr, time_frame=time_frame, pvm=date, hinta=price, nimi=name, osoite=address,  kaupunki=city, puhelin=phone, email=email, error=error_message)
    if not accepted:
        error = True
        error_message = "Hyväksy palveluehdot"
        return render_template("vahvistus.html", noutolaji=ttype, kuvaus=desc, postinumero=postcode, date_id=date_id, day_nr=day_nr, pvm=date, time_frame=time_frame, hinta=price, nimi=name, osoite=address,  kaupunki=city, puhelin=phone, email=email, error=error_message)
    cust_id = customers.insert(name, address, postcode, city, phone, email, instructions)
    orders.insert(cust_id, date_id, time_frame, ttype, desc, time_req, price, 0)
#    date = cal.get_date(date_id)
#    day_nr = date.isoweekday()
    return render_template("valmis.html", day_nr=day_nr, pvm=date, time_frame=time_frame, noutolaji=ttype, kuvaus=desc, hinta=price, nimi=name, osoite=address, postinumero=postcode, kaupunki=city, puhelin=phone, email=email, viesti=instructions)

# Varauskalenteri aloitus
@app.route("/lista")
def worklist_today():
    d_id = cal.get_today_id()
    date = cal.get_date(d_id)
    day_nr = date.isoweekday()
    if day_nr == 6:
        d_id += 2
        date = cal.get_date(d_id)
        day_nr = 1
    elif day_nr == 7:
        d_id += 1
        date = cal.get_date(d_id)
        day_nr = 1
    tlist1 = orders.get_work_list(d_id, 1)
    tlist2 = orders.get_work_list(d_id, 2)
    tlist3 = orders.get_work_list(d_id, 3)
    return render_template("varaukset.html", date_id=d_id, pvm=date, day_nr=day_nr, tasks1=tlist1, tasks2=tlist2, tasks3=tlist3)

# Varauskalenteri seuraava päivä
@app.route("/lista/<int:d_id>/<int:step>")
def worklist(d_id, step):
    date = cal.get_date(d_id)
    day_nr = date.isoweekday()
    if day_nr == 6:
        if (step == 1):
            d_id -= 1
            day_nr = 5
        elif (step == 2):
            d_id += 2
            day_nr = 1
        date = cal.get_date(d_id)
    elif day_nr == 7:
        if step == 1:
            d_id -= 2
            day_nr = 5
        elif step == 2:
            d_id += 1
            day_nr = 1
        date = cal.get_date(d_id)
    tlist1 = orders.get_work_list(d_id, 1)
    tlist2 = orders.get_work_list(d_id, 2)
    tlist3 = orders.get_work_list(d_id, 3)
    return render_template("varaukset.html", date_id=d_id, pvm=date, day_nr=day_nr, tasks1=tlist1, tasks2=tlist2, tasks3=tlist3)

# Kalenterin täyttö
@app.route("/cal")
def calfill():
    cal.fill(2022, 1096, 2152)
    return redirect("/")

def isBlank (myString):
    return not (myString and myString.strip())


