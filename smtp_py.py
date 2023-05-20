from dotenv import load_dotenv
from email.message import EmailMessage
import smtplib, os

load_dotenv('.env')

def send_mail(subject:str, message:str, to_email:str) -> bool:
    sender = os.environ.get("smtp_email")
    password = os.environ.get("smtp_password")

    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()

    msg = EmailMessage()
    msg.set_content(message)
    msg["To"] = to_email
    msg['Subject'] = subject
    msg['From'] = sender
    try:
        server.login(sender,password)
        server.sendmail(sender, "layplay22072007@gmail.com",message)
        return True
    except Exception as error:
        return f"Error: {error}"
# print(send_mail("SMTP Python Testing","SMTP Python","brawlball22@mail.ru"))

emails = ["ktoktorov144@gmail.com","toktorovkurmanbek92@gmail.com","ashatkydyrov433@gmail.com","toktoroveldos15@gmail.com"]
for email in emails:
    email=email
    print(send_mail("Hello GEEKS","SMTP Python",email))