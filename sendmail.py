from app import app
from flask_mail import Mail, Message
from os import getenv

email_address = getenv("SENDER_EMAIL")
psw = getenv("SENDER_PSW")
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": email_address,
    "MAIL_PASSWORD": psw
}
app.config.update(mail_settings)
mail = Mail(app)

def email(recipient, msg_txt):
    msg = Message('Easynouto varausvahvistus', sender = "Easynouto", recipients = [recipient])
    msg.body = msg_txt
    mail.send(msg)
    return "Sent"
