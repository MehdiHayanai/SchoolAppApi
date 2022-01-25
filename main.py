import requests
import json
import hashlib
from time import sleep, time
import smtplib
import os
from dotenv import load_dotenv
import schedule


load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
CONTACTEMAIL = os.getenv("CONTACTEMAIL")
CONTACTPASSWORD = os.getenv("CONTACTPASSWORD")
current_hash = ""

with open("hash.txt", "r") as f:
    current_hash = f.readline()


def send_email(
    CONTACTEMAIL=CONTACTEMAIL, CONTACTPASSWORD=CONTACTPASSWORD, receiver=EMAIL, msg=None
):
    t = time()
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        subject = "SchooalApp changes detecter"

        smtp.login(CONTACTEMAIL, CONTACTPASSWORD)
        if msg == None:
            body = "something changed in SchooalApp."
        else:
            body = msg
        msg = "Subject : {}\n\n{}".format(subject, body)

        smtp.sendmail(CONTACTEMAIL, receiver, msg)

    print("email sent in {} sec".format(time() - t))


def login(email, password):
    s = requests.Session()
    payload = {"email": email, "password": password}

    res = s.post(
        "https://schoolapp-fetcher.vercel.app/api/_internal/check", json=payload
    )
    # print(res.text)
    json_string = json.dumps(res.text, sort_keys=True, indent=4)

    return json_string


def main():
    global EMAIL, PASSWORD, current_hash
    json_string = login(EMAIL, PASSWORD)
    print("starting")
    dict_string = json_string.replace("""\\""", "")[1:-1]
    latest_hash = hashlib.md5(dict_string.encode()).hexdigest()

    if current_hash != latest_hash:
        send_email()
        with open("hash.txt", "w") as f:
            f.write(latest_hash)
            current_hash = latest_hash
    else:
        print("no update")
        send_email(msg="nothing changed")
    print("sleeping for 10 secs")


schedule.every(30).seconds.do(main)

while True:
    schedule.run_pending()
    sleep(5)
