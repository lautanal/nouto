from app import app
from flask_mail import Mail, Message
from os import getenv

easynouto_email = getenv("EASYNOUTO_EMAIL")
email_address = getenv("SENDER_EMAIL")
psw = getenv("SENDER_PSW")
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": email_address,
    "MAIL_PASSWORD": psw,
    "MAIL_DEFAULT_SENDER": easynouto_email
}
app.config.update(mail_settings)
mail = Mail(app)

def customer_email(email, ttype, desc, day_nr, pvm, time_frame, price, name, address, postcode, city, phone, instructions):
    msg = Message("Easynouto tilausvahvistus", sender=("Easynouto", easynouto_email), recipients = [email])
    emsg = "TILAUSVAHVISTUS\n\nNoudon tiedot: "
    if ttype == "1":
        emsg = emsg + "\n1 esine\n"
    elif ttype == "2":
        emsg= emsg + "\n2-3 esinettä\n"
    elif ttype == "3":
        emsg = emsg + "\n30 minuutin nouto\n"
    emsg = emsg + desc + "\nHinta: " + price + " €\nNoudon ajankohta: "
    if day_nr == 1:
        emsg = emsg + "maanantai " + str(pvm.day) + "." + str(pvm.month) + "." + str(pvm.year)
    elif day_nr == 2:
        emsg = emsg + "tiistai " + str(pvm.day) + "." + str(pvm.month) + "." + str(pvm.year)
    elif day_nr == 3:
        emsg = emsg + "keskiviikko " + str(pvm.day) + "." + str(pvm.month) + "." + str(pvm.year)
    elif day_nr == 4:
        emsg = emsg + "torstai "  + str(pvm.day) + "." + str(pvm.month) + "." + str(pvm.year)
    elif day_nr == 5:
        emsg = emsg + "perjantai "  + str(pvm.day) + "." + str(pvm.month) + "." + str(pvm.year)
    if time_frame == "1":
        emsg = emsg + " klo 08-11 \nTilaaja:\n"
    elif time_frame == "2":
        emsg = emsg + " klo 11-14 \nTilaaja:\n"
    elif time_frame == "3":
        emsg = emsg + " klo 14-17 \nTilaaja:\n"
    elif time_frame == "4":
        emsg = emsg + " klo 17-20 \nTilaaja:\n"
    emsg = emsg + name + "\n" + address + ", " + postcode + " " + city + "\nPuh: " + phone + "\nEmail: " + email
    if not isBlank(instructions):
        emsg = emsg + "\nOhjeet:\n" + instructions    
    emsg2 = emsg + "\n\nKiitos tilauksesta!\n\nEasynouto\nInfopuhelin: 0600391500 (€0.05+ppm)\nWhatsApp: 050 4656 001\nSähköposti: info@easynouto.fi"
    msg.body = emsg2
    msg.reply_to = easynouto_email
    if not isBlank(email):
        mail.send(msg)

    msg = Message("TILAUS", sender=("Easynouto", easynouto_email), recipients = [easynouto_email])
    msg.body = emsg
    msg.reply_to = easynouto_email
    mail.send(msg)

    return "Sent"

def isBlank (myString):
    return not (myString and myString.strip())

