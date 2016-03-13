import smtplib
from requests import get

ip = get('http://api.ipify.org').text 
to = 'yyyy@gmail.com'
gmail_user = 'yyy@gmail.com'
gmail_pwd ='xxxxxxx'
smtpserver = smtplib.SMTP("smtp.gmail.com",587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo()
smtpserver.login(gmail_user, gmail_pwd)
header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:@pp \n'
msg = header + '\n @pp='+ ss  +'\n\n'
print msg
smtpserver.sendmail(gmail_user, to, msg)
print 'done!'
smtpserver.close()
