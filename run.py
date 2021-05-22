import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path

import json,sys,os

sender = ""
user = ""
password = ""
smtp = ""
skylight = ""

sent = []

with open("config.json",'r') as f:
    obj = json.load(f)
    
    sender = obj['sender']
    smtp = obj['smtp']
    user = obj['user']
    password = obj['pass']
    skylight = obj['skylight']

def send_email(email_recipient,
               email_subject,
               email_message,
               photos = []):

    email_sender = sender

    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_recipient
    msg['Subject'] = email_subject

    msg.attach(MIMEText(email_message, 'plain'))


    sending = []
    cnt = 0 # only want to take 2 at a time...

    for file in os.listdir(photos):

        filename = photos+os.path.basename(file)

        if filename in sent:
            continue

        sending.append(filename)

        print(filename)

        attachment = open(filename, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        "attachment; filename= %s" % filename)
        msg.attach(part)
        
        cnt+=1

        if cnt > 1:
            break

    server = smtplib.SMTP(smtp, 587)
    server.ehlo()
    server.starttls()
    server.login(user, password)
    text = msg.as_string()
    server.sendmail(email_sender, email_recipient, text)
    print('Email Sent!')
    server.quit()

    toDelete = sending
    for item in toDelete:
        sent.append(item)
        #os.remove(item)
        #print("Deleted {}.".format(item))


while len(os.listdir("Images/")) > 0:

    send_email(skylight,
            'Test', #Subject
            '', #Body
            'Images/') #Attachment