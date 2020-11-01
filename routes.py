from app import app
from flask_mail import Mail, Message
from flask import render_template, request, redirect, flash, Markup
from datetime import date, timedelta
import users, cal, customers, orders, prices, admins, sendmail, offtime

@app.route("/email")
def emailtest():
    receipient = "lasselautanala@gmail.com"
    msg = "Heippa, tämä on Easynoudon 5. testilähetys"
#    sendmail.emailtest(receipient,msg)
    return "Sent"

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
        if postin == 2700:
            kaupunki = "Kauniainen" 
    elif postinumero in postinumerot:
        p_accepted = True
        kaupunki = postinumerot.get(postinumero)
        p_extra = 20

    if not p_accepted:
        return render_template("index.html", noutolaji=noutolaji, kuvaus=kuvaus, postinumero=postinumero, error="Postinumero hakualueen ulkopuolella")

    viikko_nr = cal.get_week()
    paivat = cal.get_days(viikko_nr)
    max_var = 135
    if noutolaji == "3":
        max_var = 120
    varaukset = offtime.get_offtime(viikko_nr)
    varaukset = orders.check_orders(viikko_nr, max_var, varaukset)
    check = 19
    for slot in range(20):
        if (varaukset[19-slot] == 0):
            check = 19 - slot
    hinnat = prices.prices(viikko_nr, paivat[0][1], noutolaji, kaupunki, p_extra)

    return render_template("ajanvaraus.html", noutolaji=noutolaji, kuvaus=kuvaus, postinumero=postinumero, kaupunki=kaupunki, viikko_nr=viikko_nr, vdelta=0, paivat=paivat, varattu=varaukset, hinnat=hinnat, valinta=check, p_extra=p_extra)

# Seuraava viikko
@app.route("/seuraava/<int:wnr>/<int:vdelta>/<string:noutolaji>/<string:kuvaus>/<string:postinumero>/<string:kaupunki>/<int:p_extra>")
def seuraavaviikko(wnr, vdelta, noutolaji, kuvaus, postinumero, kaupunki, p_extra):
    viikko_nr=int(wnr)
    if (vdelta < 8):
        vdelta += 1
        if (viikko_nr % 100 < 52):
            viikko_nr += 1
        else:
            viikko_nr = cal.get_next_week(viikko_nr)

    paivat = cal.get_days(viikko_nr)
    max_var = 135
    if noutolaji == "3":
        max_var = 120
    varaukset = offtime.get_offtime(viikko_nr)
    varaukset = orders.check_orders(viikko_nr, max_var, varaukset)
    check = 1
    for slot in range(20):
        if (varaukset[19-slot] == 0):
            check = 19- slot
    hinnat = prices.prices(viikko_nr, paivat[0][1], noutolaji, kaupunki, int(p_extra))

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
    max_var = 135
    if noutolaji == "3":
        max_var = 120
    varaukset = offtime.get_offtime(viikko_nr)
    varaukset = orders.check_orders(viikko_nr, max_var, varaukset)
    check = 19
    for slot in range(20):
        if (varaukset[19-slot] == 0):
            check = 19 - slot
    hinnat = prices.prices(viikko_nr, paivat[0][1], noutolaji, kaupunki, int(p_extra))

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
    day_nr = int(tsel)//4
    date_id = paivat[day_nr][1]
    pvm = cal.get_date(date_id)
    time_frame = int(tsel) - 4*day_nr + 1
    phinta = prices.get_price(date_id, time_frame, noutolaji, kaupunki, int(p_extra))
    day_nr += 1

    return render_template("vahvistus.html", noutolaji=noutolaji, kuvaus=kuvaus, postinumero=postinumero, kaupunki=kaupunki, date_id=date_id, time_frame=time_frame, day_nr=day_nr, pvm=pvm, hinta=phinta)

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

    pvm = cal.get_date(date_id)
    day_nr = pvm.isoweekday()

    if ttype == "1":
        time_req = 45
    elif ttype == "2":
        time_req = 45
    elif ttype == "3":
        time_req = 60

    if isBlank(name) or isBlank(address) or isBlank(phone) or isBlank(email):
        error_message = "Täytä puuttuvat tiedot"
        return render_template("vahvistus.html", noutolaji=ttype, kuvaus=desc, postinumero=postcode, date_id=date_id, day_nr=day_nr, time_frame=time_frame, pvm=pvm, hinta=price, nimi=name, osoite=address,  kaupunki=city, puhelin=phone, email=email, error=error_message)
    if not accepted:
        error_message = "Hyväksy palveluehdot"
        return render_template("vahvistus.html", noutolaji=ttype, kuvaus=desc, postinumero=postcode, date_id=date_id, day_nr=day_nr, pvm=pvm, time_frame=time_frame, hinta=price, nimi=name, osoite=address,  kaupunki=city, puhelin=phone, email=email, error=error_message)
    cust_id = customers.insert(name, address, postcode, city, phone, email, instructions)
    orders.insert(cust_id, date_id, time_frame, ttype, desc, time_req, price, 0)
    
    sendmail.customer_email(email, ttype, desc, day_nr, pvm, time_frame, price, name, address, postcode, city, phone, instructions)

    return render_template("valmis.html", day_nr=day_nr, pvm=pvm, time_frame=time_frame, noutolaji=ttype, kuvaus=desc, hinta=price, nimi=name, osoite=address, postinumero=postcode, kaupunki=city, puhelin=phone, email=email, viesti=instructions)

# Lisähinnat ja alennukset
@app.route("/hinnat")
def hinnat():
    if admins.admin_id() == 0:
        return render_template("adloginh.html", login="yes")
    else:
        viikko_nr = cal.get_week()
        paivat = cal.get_days(viikko_nr)
        hinnat = prices.get_add_prices(viikko_nr)

        return render_template("hinnat.html", viikko_nr=viikko_nr, vdelta=0, paivat=paivat, hinnat=hinnat)

@app.route("/hinnats/<int:wnr>/<int:vdelta>")
def hinnats(wnr, vdelta):
    if admins.admin_id() == 0:
        return render_template("adloginh.html", login="yes")
    else:
        viikko_nr=int(wnr)
        if (vdelta < 12):
            vdelta += 1
            if (viikko_nr % 100 < 52):
                viikko_nr += 1
            else:
                viikko_nr = cal.get_next_week(viikko_nr)

        paivat = cal.get_days(viikko_nr)
        hinnat = prices.get_add_prices(viikko_nr)

        return render_template("hinnat.html", viikko_nr=viikko_nr, vdelta=vdelta, paivat=paivat, hinnat=hinnat)

@app.route("/hinnate/<int:wnr>/<int:vdelta>")
def hinnate(wnr, vdelta):
    if admins.admin_id() == 0:
        return render_template("adloginh.html", login="yes")
    else:
        viikko_nr=int(wnr)
        if vdelta > 0:
            vdelta -= 1
            if (viikko_nr % 100 > 1):
                viikko_nr -= 1
            else:
                viikko_nr = cal.get_prev_week(viikko_nr)

        paivat = cal.get_days(viikko_nr)
        hinnat = prices.get_add_prices(viikko_nr)

        return render_template("hinnat.html", viikko_nr=viikko_nr, vdelta=vdelta, paivat=paivat, hinnat=hinnat)

@app.route("/lisahinnat/<int:wnr>/<int:vdelta>", methods=["post"])
def lisahinnat(wnr, vdelta):
    if admins.admin_id() == 0:
        return render_template("adloginh.html", login="yes")
    else:
        hinnat = [0,0,0,0,0]
        hinnat[0] = int(request.form["d0"])
        hinnat[1] = int(request.form["d1"])
        hinnat[2] = int(request.form["d2"])
        hinnat[3] = int(request.form["d3"])
        hinnat[4] = int(request.form["d4"])
        paivat = cal.get_days(wnr)
        prices.update(wnr, paivat[0][1], hinnat)
        
        return render_template("hinnat.html", viikko_nr=wnr, vdelta=vdelta, paivat=paivat, hinnat=hinnat, msg="Hinnat päivitetty")

# Varauskalenteri aloitus
@app.route("/varaukset")
def worklist_today():
    if admins.admin_id() == 0:
        return render_template("adloginv.html", login="yes")
    else:
        wday = cal.get_wday()
        d_id = wday[0]
        pvm = wday[1]
        day_nr = pvm.isoweekday()

        tlist1 = orders.get_work_list(d_id, 1)
        tlist2 = orders.get_work_list(d_id, 2)
        tlist3 = orders.get_work_list(d_id, 3)
        tlist3 = orders.get_work_list(d_id, 4)
        return render_template("varaukset.html", date_id=d_id, pvm=pvm, day_nr=day_nr, tasks1=tlist1, tasks2=tlist2, tasks3=tlist3)

# Varauskalenteri seuraava päivä
@app.route("/varaukset/<int:d_id>/<int:step>")
def worklist(d_id, step):
    if admins.admin_id() == 0:
        return render_template("adlogin.html", login="yes")
    else:
        if step == 1:
            wday = cal.get_wday_prev(d_id)
            d_id = wday[0]
            pvm = wday[1]
        else:
            wday = cal.get_wday_next(d_id)
            d_id = wday[0]
            pvm = wday[1]
        day_nr = pvm.isoweekday()

        tlist1 = orders.get_work_list(d_id, 1)
        tlist2 = orders.get_work_list(d_id, 2)
        tlist3 = orders.get_work_list(d_id, 3)
        tlist4 = orders.get_work_list(d_id, 4)
        return render_template("varaukset.html", date_id=d_id, pvm=pvm, day_nr=day_nr, tasks1=tlist1, tasks2=tlist2, tasks3=tlist3, tasks4=tlist4)

# Varauksen poisto
@app.route("/poista/<int:o_id>")
def poista(o_id):
    if admins.admin_id() == 0:
        return render_template("adlogin.html", login="yes")
    else:
        ol = orders.get_order(o_id)
        d_id = ol[0]
        ttype = ol[1]
        desc = ol[2]
        time_frame = ol[3]
        price = ol[4]
        name = ol[5]
        address = ol[6]
        postcode = ol[7]
        city = ol[8]
        phone = ol[9]
        email = ol[10]
        instructions = ol[11]

        pvm = cal.get_date(d_id)
        day_nr = pvm.isoweekday()

        return render_template("poista.html", oid=o_id, day_nr=day_nr, pvm=pvm, time_frame=time_frame, noutolaji=ttype, kuvaus=desc, hinta=price, nimi=name, osoite=address, postinumero=postcode, kaupunki=city, puhelin=phone, email=email, viesti=instructions)

# Varauksen poiston vahvistus
@app.route("/poistovahvistus/<int:o_id>", methods=["post"])
def poistovahvistus(o_id):
    if admins.admin_id() == 0:
        return render_template("adlogin.html", login="yes")
    else:
        ol = orders.get_order_data(o_id)
        orders.order_delete(o_id, ol[2])

        d_id = ol[0]
        pvm = ol[1]
        day_nr = pvm.isoweekday()

        tlist1 = orders.get_work_list(d_id, 1)
        tlist2 = orders.get_work_list(d_id, 2)
        tlist3 = orders.get_work_list(d_id, 3)
        tlist4 = orders.get_work_list(d_id, 4)
        return render_template("varaukset.html", date_id=d_id, pvm=pvm, day_nr=day_nr, tasks1=tlist1, tasks2=tlist2, tasks3=tlist3, tasks4=tlist4)

# Vapaa-päivät ja slotit
@app.route("/vapaat")
def vapaat():
    if admins.admin_id() == 0:
        return render_template("adloginh.html", login="yes")
    else:
        viikko_nr = cal.get_week()
        paivat = cal.get_days(viikko_nr)
        offlist = offtime.get_offtime(viikko_nr)

        return render_template("vapaat.html", viikko_nr=viikko_nr, vdelta=0, paivat=paivat, offlist=offlist)

@app.route("/vapaats/<int:wnr>/<int:vdelta>")
def vapaats(wnr, vdelta):
    if admins.admin_id() == 0:
        return render_template("adloginh.html", login="yes")
    else:
        viikko_nr=int(wnr)
        if (vdelta < 12):
            vdelta += 1
            if (viikko_nr % 100 < 52):
                viikko_nr += 1
            else:
                viikko_nr = cal.get_next_week(viikko_nr)
        paivat = cal.get_days(viikko_nr)
        offlist = offtime.get_offtime(viikko_nr)

        return render_template("vapaat.html", viikko_nr=viikko_nr, vdelta=vdelta, paivat=paivat, offlist=offlist)

@app.route("/vapaate/<int:wnr>/<int:vdelta>")
def vapaate(wnr, vdelta):
    if admins.admin_id() == 0:
        return render_template("adloginh.html", login="yes")
    else:
        viikko_nr=int(wnr)
        if vdelta > 0:
            vdelta -= 1
            if (viikko_nr % 100 > 1):
                viikko_nr -= 1
            else:
                viikko_nr = cal.get_prev_week(viikko_nr)
        paivat = cal.get_days(viikko_nr)
        offlist = offtime.get_offtime(viikko_nr)

        return render_template("vapaat.html", viikko_nr=viikko_nr, vdelta=vdelta, paivat=paivat, offlist=offlist)

@app.route("/vapaat/<int:wnr>/<int:vdelta>", methods=["post"])
def vapaat_talletus(wnr, vdelta):
    if admins.admin_id() == 0:
        return render_template("adloginh.html", login="yes")
    else:
        offlist = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        if request.form.get("ma1"):
            offlist[0] = 1
        if request.form.get("ma2"):
            offlist[1] = 1
        if request.form.get("ma3"):
            offlist[2] = 1
        if request.form.get("ma4"):
            offlist[3] = 1
        if request.form.get("ti1"):
            offlist[4] = 1
        if request.form.get("ti2"):
            offlist[5] = 1
        if request.form.get("ti3"):
            offlist[6] = 1
        if request.form.get("ti4"):
            offlist[7] = 1
        if request.form.get("ke1"):
            offlist[8] = 1
        if request.form.get("ke2"):
            offlist[9] = 1
        if request.form.get("ke3"):
            offlist[10] = 1
        if request.form.get("ke4"):
            offlist[11] = 1
        if request.form.get("to1"):
            offlist[12] = 1
        if request.form.get("to2"):
            offlist[13] = 1
        if request.form.get("to3"):
            offlist[14] = 1
        if request.form.get("to4"):
            offlist[15] = 1
        if request.form.get("pe1"):
            offlist[16] = 1
        if request.form.get("pe2"):
            offlist[17] = 1
        if request.form.get("pe3"):
            offlist[18] = 1
        if request.form.get("pe4"):
            offlist[19] = 1
#        print("VAPAAT: ", offlist)
        paivat = cal.get_days(wnr)
        offtime.update(wnr, paivat[0][1], offlist)
        
        return render_template("vapaat.html", viikko_nr=wnr, vdelta=vdelta, paivat=paivat, offlist=offlist, msg="Vapaat päivitetty")

# Kalenterin täyttö
@app.route("/cal")
def calfill():
    cal.fill(2022, 1096, 2152)
    return redirect("/")

def isBlank (myString):
    return not (myString and myString.strip())

