'''import smtplib

# wasted!!


import ssl
import poplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

smtps = {'gmail': 'smtp.gmail.com', 'outlook': 'smtp.office365.com', 'yahoo': 'smtp.mail.yahoo.com',
         'hotmail': 'smtp.live.com'}
pops = {'gmail': 'pop.gmail.com', 'outlook': 'outlook.office365.com', 'yahoo': 'smtp.mail.yahoo.com',
         'hotmail': 'smtp.live.com'}

#ask the user to enable smtp authentication

# def mailrecv(mailid, password):



def mailsnd(mailid, password, tomail, header, content):
    for i in smtps:
        if i in mailid:
            stmp = smtps[i]
    server = smtplib.SMTP(stmp, 587)
    context = ssl.create_default_context()
    server.starttls(context = context)
    server.login(mailid, password)

    msg = MIMEMultipart()
    msg['From'] = str(mailid)
    msg['To'] = str(tomail)
    msg['Subject'] = str(header)
    msg.attach(MIMEText(content, 'plain'))
    text = msg.as_string()
    server.sendmail(mailid, tomail ,text)

mailsnd('unekenappa@gmail.com','MailTest','kkakss1@outlook.com','hi','proof of concept by kk')'''

