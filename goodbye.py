from database import get_ref, get_emails
from dotenv import load_dotenv
from time import time
import smtplib
import os
from email.message import Message

load_dotenv()
CONTACTEMAIL = os.getenv("CONTACTEMAIL")
CONTACTPASSWORD = os.getenv("CONTACTPASSWORD")


def send_email(
    receiver, CONTACTEMAIL=CONTACTEMAIL, CONTACTPASSWORD=CONTACTPASSWORD, msg=None
):
    t = time()
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        subject = "SchooalApp changes detector"

        smtp.login(CONTACTEMAIL, CONTACTPASSWORD)
        if msg == None:
            body = "something changed in SchooalApp."
        else:
            body = msg
        m = Message()
        m["From"] = CONTACTEMAIL
        m["To"] = receiver
        m["X-Priority"] = "1"
        m["Subject"] = subject
        m.set_payload(body)
        smtp.sendmail(CONTACTEMAIL, receiver, m.as_string())

    print("email sent in {} sec".format(time() - t))


ref = get_ref()
emails = []
for i in ["1A", "2A", "3A", "4A"]:
    year_emails = get_emails(ref, i)
    for email in year_emails:
        emails.append(email)
url = "https://docs.google.com/forms/d/e/1FAIpQLSepxoCJVu8jhibM8N6IiwTLwQRTfZJ3B3zaQmMwwgrSg-WhGw/viewform?usp=sf_link"
msg = f"Thank you for using School App Notifier, we hope our service was useful for you and we invite you to give us your feedback here {url}. \n\nUnfortunately our service is no longer available see you soon with a better version and good luck for your exames."
for email in emails:
    send_email(email, msg=msg)

