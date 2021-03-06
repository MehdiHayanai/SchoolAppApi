from datetime import datetime
import requests
import json
import hashlib
from time import sleep, time
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
import schedule
from database import get_hashes, get_ref, update_hash, get_emails

## LOADING ENV VAR
load_dotenv()

EMAIL = os.getenv("EMAIL")
EMAIL1A = os.getenv("EMAIL1A")
EMAIL2A = os.getenv("EMAIL2A")
EMAIL3A = os.getenv("EMAIL3A")
EMAIL4A = os.getenv("EMAIL4A")
PASSWORD1A = os.getenv("PASSWORD1A")
PASSWORD2A = os.getenv("PASSWORD2A")
PASSWORD3A = os.getenv("PASSWORD3A")
PASSWORD4A = os.getenv("PASSWORD4A")
CONTACTEMAIL = os.getenv("CONTACTEMAIL")
CONTACTPASSWORD = os.getenv("CONTACTPASSWORD")
CONTACTEMAIL1 = os.getenv("CONTACTEMAIL1")
CONTACTPASSWORD1 = os.getenv("CONTACTPASSWORD1")
CONTACTEMAIL2 = os.getenv("CONTACTEMAIL2")
CONTACTPASSWORD2 = os.getenv("CONTACTPASSWORD2")
CONTACTEMAIL3 = os.getenv("CONTACTEMAIL3")
CONTACTPASSWORD3 = os.getenv("CONTACTPASSWORD3")


EMAILS = [EMAIL1A, EMAIL2A, EMAIL3A, EMAIL4A]
PASSWORDS = [PASSWORD1A, PASSWORD2A, PASSWORD3A, PASSWORD4A]

# firebase ref

REF = get_ref()
## SETTING THE HASHES

HASHES = get_hashes(REF)
starting_from = 1


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
            body = "something has changed in SchoolApp.\n\n\nNote : this program is in the testing phase if you notice any bad behavior, please contact us on contact@gadz.it."
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
    json_string = json.dumps(res.text, sort_keys=True, indent=4)

    return json_string


def main(EMAILS=EMAILS, PASSWORDS=PASSWORDS, ref=REF):
    global HASHES
    global starting_from
    json_strings = []
    for ind, email in enumerate(EMAILS):
        login_state = True
        while login_state:
            try:
                json_string = login(email, PASSWORDS[ind])
                json_strings.append(json_string)
                login_state = False
            except:
                print(f"login failed for {email}")
                sleep(2)

    print("logged in all accounts")
    for ind, json_string in enumerate(json_strings):
        year = f"{starting_from+ind}A"
        dict_string = json_string.replace("""\\""", "")[1:-1]
        latest_hash = hashlib.md5(dict_string.encode()).hexdigest()

        if HASHES[starting_from - 1 + ind] != latest_hash:
            print(HASHES[starting_from - 1 + ind], latest_hash)
            update_hash(ref, latest_hash, year)
            HASHES[starting_from - 1 + ind] = latest_hash
            receivers = get_emails(ref, year)
            sent = 0
            if receivers != None:
                for receiver in receivers:
                    if receiver != None:
                        try:
                            if year == "1A":
                                send_email(
                                    receiver,
                                    CONTACTEMAIL=CONTACTEMAIL2,
                                    CONTACTPASSWORD=CONTACTPASSWORD2,
                                )
                            elif year == "4A":
                                send_email(
                                    receiver,
                                    CONTACTEMAIL=CONTACTEMAIL3,
                                    CONTACTPASSWORD=CONTACTPASSWORD3,
                                )
                            elif year == "2A":
                                send_email(
                                    receiver,
                                    CONTACTEMAIL=CONTACTEMAIL1,
                                    CONTACTPASSWORD=CONTACTPASSWORD1,
                                )
                            else:
                                send_email(
                                    receiver,
                                    CONTACTEMAIL=CONTACTEMAIL2,
                                    CONTACTPASSWORD=CONTACTPASSWORD2,
                                )
                            sent += 1
                        except:
                            print(f"failed to send an email to {receiver}")

                if year == "1A" or year == "4A":
                    send_email(
                        EMAIL, msg=f"Email sent to {year} {sent} of {len(receivers)}",
                    )
                else:
                    send_email(
                        EMAIL,
                        CONTACTEMAIL=CONTACTEMAIL1,
                        CONTACTPASSWORD=CONTACTPASSWORD1,
                        msg=f"Email sent to {year} {sent} of {len(receivers)}",
                    )

                print(f"Email sent to {year}")
        else:
            print(f"no update for {year}")
    print("sleeping for 60 secs")


send_email(EMAIL, msg=f"starting {datetime.now()}")

schedule.every(60).seconds.do(main)

while True:
    schedule.run_pending()
    sleep(60)

