import logging
from flask import Flask, render_template

from flask_ask import Ask, statement, question, session, request, context

###########Vikas Email start 
import smtplib

from email.utils import formatdate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

from email import encoders
import os, datetime
from asn1crypto._ffi import null



import pymongo
import pprint

from pymongo import MongoClient, collection
client = MongoClient()
client = MongoClient('mongodb://localhost:27017/')
db = client.meetingrooms
collection = db.meetingRoomsDetails


#config = fileutil.social

param = {
    "to": "vikasyadav079@outlook.com",
    "subject": "Party reminder",
    "location": "Koramangala 5th Block, Bangalore",
    "description": "Hangout",
    "meetingStartDate": "20150512T083000Z",
    "meetingEndDate": "20150512T093000Z"
}

########### Vikas email end 


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def launched():
 
    return question('Welcome to Foo')


@ask.intent("helloIntent")
def check_intent():
    print("Vikas Yadav ..................................................................")
    print (request["intent"]["slots"]["firstName"])
    print("Vikas Yadav ..................................................................")
    return statement("")


#def hello_intent(firstName, lastName):
 #   send_invite(param)
 #   db_services ()
    #session.attributes['firstName'] = firstName
 #   return question("My Name is " +  firstName +" " + lastName )
def send_invite(param):
    CRLF = "\r\n"
    attendees = param['to']
    #attendees = ""
    try:
        #for att in param['to']:
        att=param['to']
        #attendees += "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE;CN="+att+";X-NUM-GUESTS=0:mailto:"+att+CRLF
    except Exception as e:
        print (e)
    fro = "vikasyadav.a079@outlook.com"
    
    msg = MIMEMultipart('mixed')
    msg['Reply-To']=fro
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = 'Vikas:Meeting invitation from Vikas'
    msg['From'] = fro
    msg['To'] = attendees

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    f= os.path.join(__location__, 'invite.ics')   
    ics_content = open(f).read()
    try:
        replaced_contents = ics_content.replace('startDate', param['meetingStartDate'])
        replaced_contents = replaced_contents.replace('endDate', param['meetingEndDate'])
        replaced_contents = replaced_contents.replace('telephonic', param['location'])
        replaced_contents = replaced_contents.replace('now', datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ"))
    except Exception as e:
        print(e)
    if param.get('description') is not None:
        replaced_contents = replaced_contents.replace('describe', param.get('description'))
    else:
        replaced_contents = replaced_contents.replace('describe', '')
    replaced_contents = replaced_contents.replace('attend',  msg['To'])
    replaced_contents = replaced_contents.replace('subject',  param['subject'])
    print ("Vikas Read File "+ ics_content)
    part_email = MIMEText(replaced_contents,'calendar;method=REQUEST')

    
    msgAlternative = MIMEMultipart('alternative')
   
    
    ical_atch = MIMEBase('text/calendar',' ;name="%s"'%"invitation.ics")
    ical_atch.set_payload(replaced_contents)
    encoders.encode_base64(ical_atch)
    ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"'%f)
    

    
    msgAlternative.attach(part_email)
    msgAlternative.attach(ical_atch)
    msg.attach(msgAlternative)
    mailServer = smtplib.SMTP('smtp-mail.outlook.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login('vikasyadav.a079@outlook.com', 'rahul@938935')
    mailServer.sendmail(fro, param['to'], msg.as_string())
    mailServer.close()



    
#mail send 

@ask.session_ended
def session_ended():
    return "{}", 200    

@ask.on_session_started
def new_session():
    print("new session started Vikas")
    


if __name__ == '__main__':

    app.run(debug=True)
    
