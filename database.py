import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime


def get_ref():
    cred = credentials.Certificate(
        "schoolappnotifier-firebase-adminsdk-6wycw-2edf45dfca.json"
    )
    firebase_admin.initialize_app(
        cred,
        {
            "databaseURL": "https://schoolappnotifier-default-rtdb.europe-west1.firebasedatabase.app/"
        },
    )
    ref = db.reference()
    return ref


def update_emails(new_emails, year, ref):
    email_ref = ref.child("users/{}".format(year))
    emails = email_ref.get()
    if emails == None:
        ref.child(f"users").update({year: new_emails})
        return
    for new_email in new_emails:
        emails.append(new_email)
    ref.child("users").update({"{}".format(year): emails})


def update_hash(ref, new_hash, year):
    ref.child(f"hash/{year}").update({"code": new_hash, "time": str(datetime.now())})


def get_hashes(ref):
    hashes_dict = dict(ref.child("hash").get())
    ans = [hashes_dict[key]["code"] for key in hashes_dict]
    return ans


def get_emails(ref, year):
    ans = ref.child(f"users/{year}").get()
    return ans

