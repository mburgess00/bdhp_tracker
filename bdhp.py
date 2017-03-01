#!/bin/python
import smtplib
from bs4 import BeautifulSoup
import requests
from datetime import datetime

r = requests.get('http://bigdogshugepaws.com/tracker')
data = r.text
soup = BeautifulSoup(data)
dogs = soup.find_all("tr")
olddogs = [line.rstrip('\n') for line in open('/tmp/olddogs.txt')]
currdogs = []
prefix = "http://bigdogshugepaws.com"
for element in dogs[1:]:
    currdogs.append(prefix + element.a["href"])
newdogs = list(set(currdogs) - set(olddogs))
file = open('/tmp/olddogs.txt', 'w')
for item in currdogs:
    file.write("%s\n" % item)
file.close
logfile = open('/var/log/bdhp.log', 'a')
logfile.write("%s\n" % datetime.utcnow())
if len(newdogs) > 0:
    fromaddr = '*************@gmail.com'
    toaddr = ['*************@gmail.com', '***************@gmail.com']
    msg = [
        "From: ************@gmail.com",
        "To: ************@gmail.com",
        "Subject: Changes in dogs at BDHP",
        "",
        ]
    for dog in newdogs:
        msg.append(dog)
        logfile.write("%s\n" % dog)
    msg = "\r\n".join(msg)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    password = '*************'
    username = '*************'
    server.login(username,password)
    server.sendmail(fromaddr, toaddr, msg)
    server.quit()
    logfile.write("Found changes, emailing...\n")
else:
    logfile.write("No changes found, exiting...\n")
logfile.close
