# from json import load
# from database import get_ref, update_emails
# from dotenv import load_dotenv
# from time import time
# import smtplib
# import os
# from email.message import Message

# load_dotenv()
# CONTACTEMAIL = os.getenv("CONTACTEMAIL")
# CONTACTPASSWORD = os.getenv("CONTACTPASSWORD")


# def send_email(
#     receiver, CONTACTEMAIL=CONTACTEMAIL, CONTACTPASSWORD=CONTACTPASSWORD, msg=None
# ):
#     t = time()
#     with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
#         smtp.ehlo()
#         smtp.starttls()
#         smtp.ehlo()
#         subject = "SchooalApp changes detector"

#         smtp.login(CONTACTEMAIL, CONTACTPASSWORD)
#         if msg == None:
#             body = "something changed in SchooalApp."
#         else:
#             body = msg
#         m = Message()
#         m["From"] = CONTACTEMAIL
#         m["To"] = receiver
#         m["X-Priority"] = "1"
#         m["Subject"] = subject
#         m.set_payload(body)
#         smtp.sendmail(CONTACTEMAIL, receiver, m.as_string())

#     print("email sent in {} sec".format(time() - t))


# ref = get_ref()

# A2 = [
#     "younesseaabibi828@gmail.com",
#     "Bahae.otaku@gmail.com",
#     "zerhjawad87@gmail.com",
#     "a.ankit@edu.umi.ac.ma",
# ]
# A3 = ["issamizarkane@gmail.com", "Ilya.ziyani@gmail.com", "imane2842001@gmail.com"]
# A4 = ["yassinetalhaouimks@gmail.com", "belmaroufchaimae@gmail.com"]

# A = [A2, A3, A4]

# s = ["2A", "3A", "4A"]


# for i in range(3):
#     text_consi = f"This service tracks schoolapp changes, you have been added to {s[i]} please activate your email notifications.\nNote that this program is only in the testing phase, please report any wrong behavior to 'Mehdi Hayani'.\n**Limitations:**\nthis program is not working yet for ratt.\nfirst year is not available yet.\nwrong results for reserve."
#     for email in A[i]:
#         send_email(email, msg=text_consi)
#     print("text sent to{}".format(s[i]))
