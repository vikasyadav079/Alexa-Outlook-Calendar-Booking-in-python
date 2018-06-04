import logging
import pprint

from flask import Flask, render_template
from flask_ask import Ask, statement, question, session, request, context
from werkzeug.contrib.profiler import available
from logging import _startTime
from gridfs import GridFS

app = Flask(__name__)
ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


##########################################################################
##########################################################################
import pymongo
import pprint

from pymongo import MongoClient, collection
client = MongoClient()
client = MongoClient('mongodb://localhost:27017/')
db = client.meetingrooms
collection = db.meetingRoomDetails
#########################################################################
##########################################################################



##########################################################################
##########################################################################
import smtplib

from email.utils import formatdate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

from email import encoders
import os, datetime
from asn1crypto._ffi import null

##########################################################################
##########################################################################

param = {
    "to": "",
    "from_sender":"",
    "subject_meeting": "",
    "location": "",
    "description": "",
    "meetingDate": "",
    "startTime": "",
    "endTime" :""
}


@ask.launch
def launched ():
    print(render_template('meeting_descrption',meeting_agenda="VikasYadavAgent",sender_name="VikasYadavSenderNAme"))
    return question(render_template('meeting_welcome')).reprompt(render_template('meeting_welcome_prompt'))

@ask.intent("AMAZON.FallbackIntent")
@ask.intent("AMAZON.CancelIntent")
@ask.intent("AMAZON.StopIntent")
def meeting_skill_cancel():
    print ("Vikasy Meeting Intent Canceled.......................................")
    return statement (render_template('meeting_invite_cancel'))


@ask.intent("AMAZON.HelpIntent")
def help_intent():
    print ("Vikasy helpIntent has been called......................................")
    return statement("Thanks for using Alexa for meeting invitation")

@ask.intent("CheckMeetingRoomsIntent")
def check_meeting_rooms(meetingDate, startTime, endTime):
    print("Vikasy meeting Date : %s startTime : %s endTime : %s " % (meetingDate, startTime, endTime))
    ######## query db 
    booked_rooms =  get_available_rooms_db(meetingDate, startTime, endTime)
    session.attributes["startTime"]=startTime
    session.attributes["endTime"]=endTime
    session.attributes["meetingDate"]=meetingDate
    all_rooms = get_all_rooms()
    available_rooms=[]
    for room in all_rooms:
        if room in booked_rooms:
            continue
        else:
            available_rooms.append(room)
    if len(available_rooms) > 0 :
        available_rooms_string = arrayToString(available_rooms)
        session.attributes['available_rooms']=available_rooms
        session.attributes['all_rooms']=all_rooms
        all_rooms_string=arrayToString(all_rooms)
        print("Available rooms are " + available_rooms_string)
        return question(render_template('meeting_check_meeting_rooms',available_rooms=available_rooms)).reprompt(render_template('meeting_confirm_meeting_prompt'))    
    else:
        return statement("No meeting rooms are availbale for now")

@ask.intent("CheckOneMeetingRoomIntent")
def check_one_meeting_room(meetingRoom,meetingDate,startTime,endTime):
    if get_single_room_status(meetingRoom,meetingDate,startTime,endTime) :
        session.attributes["meetingRoomInContext"]=meetingRoom
        return question(render_template('meeting_check_meeting_room_single_success', meeting_room='meetingRoom',meeting_date='meetingDate',start_time='startTime',end_time='endTime')).reprompt(render_template('meeting_confirm_meeting_prompt'))
    else :
        return question(render_template('meeting_check_meeting_room_single_fail'))
    
    
@ask.intent("ConfirmMeetingRoomInContext")
def confirmation_single_room_message():    
    param["startTime"]=session.attributes["startTime"]
    param["endTime"]=session.attributes["endTime"]
    param["meetingDate"]=session.attributes["meetingDate"]
    param["location"]=session.attributes["meetingRoomInContext"]
    return question(render_template('meeting_confirm_meeting'))

@ask.intent("ConfirmMeetingRoom")
def confirmation_message(meetingRoom):
    param["startTime"]=session.attributes["startTime"]
    param["endTime"]=session.attributes["endTime"]
    param["meetingDate"]=session.attributes["meetingDate"]
    param["location"]=meetingRoom
    return question(render_template('meeting_confirm_meeting'))

@ask.intent("DeclineMeetingRoom")
def decline_meeting():
    return statement(render_template('meeting_decline_meeting'))
    
@ask.intent("MeetingInviteSubjectIntent")
def get_meeting_subject_line(subjectLine):
    if (subjectLine):
        param["subject_meeting"] = subjectLine
        return question(render_template('meeting_send_invite_sender_receiver'))
    else :
        return question("Kindly tell subject line ").reprompt('Kindly enter subject line')
    
@ask.intent("SenderReceiverIntent")
def set_sender_receiver(senderName,receiverName):
    param["to"]=receiverName
    param["from_sender"]=senderName
    return question(render_template('meeting_send_invite_agenda'))
    
    
@ask.intent("MeetingAgendaIntent")
def set_agenda(agenda):
    param["description"]=agenda
    #collection.insert({'roomName' : param["location"], 'booked' :{'date' : param["meetingDate"], 'startTime' : param["startTime"], 'endTime':param["endTime"]}})
    set_meeting_booking()
    print("Vikas Meeting Agenda Intent")
    send_invite(param)
    return statement (render_template('meeting_sent_invite'))


#######db updated with meeting room marked as booked for paased duration and date
@ask.intent("RepeatAvailableMeetingRooms")
def get_available_rooms():
    available_rooms = session.attributes['available_rooms'] 
    i=0
    while i<len(available_rooms):
        print ("Vikas " + available_rooms[i]+ " ")
        i+=1
    available_rooms_string = arrayToString(available_rooms)
    print(available_rooms_string)
    if available_rooms : 
        return question(render_template('meeting_check_meeting_rooms',available_rooms=available_rooms_string))


@ask.session_ended
def session_ended():
    return "{}", 200    

@ask.on_session_started
def new_session():
    print("new session started...............")
    
    
###########################################################################
###########################################################################
    
def get_available_rooms_db(bookedDates, startTime, endTime ):
   roomArray = []
   bookedRooms = collection.find({"booked": {'$elemMatch': {'date': bookedDates , 'startTime' : startTime, 'endTime' : endTime} }})
   for bookedRoom in bookedRooms : 
       roomArray.append(bookedRoom["roomName"])
       
   return (roomArray)


def get_all_rooms():
    return (["Room1","Room2","Room3","Room4","Room5","Room6","Room7","Room8","Room9","Room10"])  

def get_single_room_status(roomName,bookedDates,startTime,endTime):
    #bookedRooms = collection.count({'$and':{{'roomName' : roomName },{"booked": {'$elemMatch': {'date': bookedDates , 'startTime' : startTime, 'endTime' : endTime}}} }})
    bookedRooms = collection.count({'roomName' : roomName, "booked": {'$elemMatch': {'date': bookedDates, 'startTime' : startTime, 'endTime' : endTime}}})
    if bookedRooms :
        return (1)
    else :
        return (0)  

def set_meeting_booking():
    collection.insert({'roomName' : param["location"], 'booked' :{'date' : param["meetingDate"], 'startTime' : param["startTime"], 'endTime':param["endTime"]}})
    return

############################################################################
############################################################################  


##############################################################################
##############################################################################
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
        replaced_contents = ics_content.replace('startTime', param['startTime'])
        replaced_contents = replaced_contents.replace('endTime', param['endTime'])
        replaced_contents = replaced_contents.replace('meetingDate', param['meetingDate'])
        replaced_contents = replaced_contents.replace('telephonic', param['location'])
        #replaced_contents = replaced_contents.replace('now', datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ"))
    except Exception as e:
        print(e)
    if param.get('description') is not None:
        replaced_contents = replaced_contents.replace('describe', param.get('description'))
    else:
        replaced_contents = replaced_contents.replace('describe', '')
    replaced_contents = replaced_contents.replace('attend',  msg['To'])
    replaced_contents = replaced_contents.replace('subject',  param['subject_meeting'])
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

######################################################################################################
######################################################################################################

def arrayToString(arrayName):
    if len(arrayName):
        st = ''
        i=0
        while i<len(arrayName):
            st = st+", "+arrayName[i]
            i+=1
        return st
    else : 
        return ''
    
    
if __name__ == '__main__':
    app.run(debug=True)
