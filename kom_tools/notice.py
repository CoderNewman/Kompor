'''
Created on 2017年9月6日

@author: liqing
'''
import smtplib
import socket
import os
from email.mime.text import MIMEText
from email.header import Header
from subprocess import Popen, PIPE
import re

EMAIL_HOST          = 'smtp.exmail.qq.com'
EMAIL_HOST_USER     = 'im@kavout.com'
EMAIL_HOST_PASSWORD = '10kcrunch2015'
EMAIL_PORT = 465

def send_email(receiver, subject, content):    
    myname = socket.getfqdn(socket.gethostname(  ))
    myaddr = get_my_ip()
    
    content += "\n\n\n"
    content += "From:" + str(myname) + "\n"
    content += "Addr:" + str(myaddr) + "\n"   
    
    print(content)

    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = Header(EMAIL_HOST_USER, 'utf-8') 
    msg['To'] = Header(",".join(receiver), 'utf-8') 
    msg['Subject'] = Header(subject,'utf-8')
    
    smtp = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)
    smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    smtp.sendmail(EMAIL_HOST_USER, receiver, msg.as_string())
    smtp.quit()
    
def get_my_ip():
    re_addr = ''
    try:
        myaddr = Popen('ifconfig', stdout=PIPE).stdout.read()
        myaddr = str(myaddr)
        myaddrs = myaddr.split('inet')
        length = len(myaddrs)
        i = 1
        while ( i < length):
            re_addr += str(myaddrs[i].lstrip().split(' ')[0]) + "; "
            i += 2

    except:
        pass
    return re_addr
