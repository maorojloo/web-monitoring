import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import time
import urllib3
import json


#---------------------------------------------------------------
with open("secrets.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

#---------------------------------------------------------------
sender_email_addr=jsonObject['sender_email_addr']
sender_email_pass=jsonObject['sender_email_pass']
receiver_email_addr=jsonObject['receiver_email_addr'] 

rechecktime=5 #secend
emailmsg="THE WEBSITE IS FUCKEDUP"  #email msg
emailtitle="WEB ALLERT [NO REPLY]"  #email title
WEBSITE_url='http://127.0.0.1:8000' #http[s]://xxxxxxxxxx.xxx
#-----------------------------------------------------------------


def send_email(Subject,mail_content):
    #The mail addresses and password
    sender_address = sender_email_addr
    sender_pass = sender_email_pass
    receiver_address = receiver_email_addr
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = Subject   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')

http = urllib3.PoolManager()
#print('the script is runn')
print('''

                        _             
                       (_)            
 _ __ _   _ _ __  _ __  _ _ __   __ _ 
| '__| | | | '_ \| '_ \| | '_ \ / _` |
| |  | |_| | | | | | | | | | | | (_| |
|_|   \__,_|_| |_|_| |_|_|_| |_|\__, |
                                 __/ |
                                |___/ 
                        ,////,
                        /// 6|
                        //  _|
                       _/_,-'
                  _.-/'/   \   ,/;,
               ,-' /'  \_   \ / _/
               `\ /     _/\  ` /
                 |     /,  `\_/
                 |     \'
 pb  /\_        /`      /\\
   /' /_``--.__/\  `,. /  \\
  |_/`  `-._     `\/  `\   `.
            `-.__/'     `\   |
                          `\  \\
                            `\ \\
                              \_\__
                               \___)

''')

def check_web ():
    try:
        r = http.request('GET',WEBSITE_url , TimeoutError=5)
        print(r.status)
        if r.status != 200:
            print("web is down")
            send_email(emailtitle,emailmsg)
        else:
            print("web is 0k")
    except :
        print("web is down")
        send_email(emailtitle,emailmsg)
     
schedule.every(rechecktime).seconds.do(check_web)
while True:
    schedule.run_pending()
    time.sleep(2)
