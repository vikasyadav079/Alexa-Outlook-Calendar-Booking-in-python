import logging
import pprint

from flask import Flask, render_template
from flask_ask import Ask, statement, question, session, request, context
from werkzeug.contrib.profiler import available
from logging import _startTime
from gridfs import GridFS

from datetime import datetime
from datetime import date
import math

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
import os
from asn1crypto._ffi import null

##########################################################################
##########################################################################

param = {
    "to": [],
    "from_sender":"",
    "subject_meeting": "",
    "location": "",
    "locationAlias":"",
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
        return question(render_template('meeting_check_meeting_rooms',available_rooms=available_rooms_string)).reprompt(render_template('meeting_confirm_meeting_prompt'))    
    else:
        return statement("No meeting rooms are availbale for now")

@ask.intent("CheckOneMeetingRoomIntent")
def check_one_meeting_room(meetingRoom,meetingDate,startTime,endTime):
    if get_single_room_status(meetingRoom,meetingDate,startTime,endTime) :
        session.attributes["startTime"]=startTime
        session.attributes["endTime"]=endTime
        session.attributes["meetingDate"]=meetingDate
        session.attributes["meetingRoomInContext"]=meetingRoom
        session.attributes["meetingRoom"]=meetingRoom
        return question(render_template('meeting_check_meeting_room_single_success', meeting_room='meetingRoom',meeting_date='meetingDate',start_time='startTime',end_time='endTime')).reprompt(render_template('meeting_confirm_meeting_prompt'))
    else :
        return question(render_template('meeting_check_meeting_room_single_fail'))
    
    
@ask.intent("ConfirmMeetingRoomInContext")
def confirmation_single_room_message():    
    param["startTime"]=session.attributes["startTime"]
    param["endTime"]=session.attributes["endTime"]
    meetingRoomValue=read_config_file(session.attributes["meetingRoomInContext"])
    meetingRoomValueAlias=read_config_file(session.attributes["meetingRoomInContext"])
    param["meetingDate"]=session.attributes["meetingDate"]
    param["location"]=meetingRoomValue
    param["locationAlias"]=meetingRoomValueAlias+"Vikas"
    return question(render_template('meeting_confirm_meeting'))

@ask.intent("ConfirmMeetingRoom")
def confirmation_message(meetingRoom):
    param["startTime"]=session.attributes["startTime"]
    param["endTime"]=session.attributes["endTime"]
    param["meetingDate"]=session.attributes["meetingDate"]
    meetingRoomValue=read_config_file(meetingRoom)
    meetingRoomValueAlias=read_config_file(meetingRoom)
    if meetingRoomValue!='' and meetingRoomValueAlias!='':
        param["location"]=meetingRoom
        param["locationAlias"]=meetingRoomValueAlias+"Vikas"
        return question(render_template('meeting_confirm_meeting'))
    else:
        return statement("Problem with skill. While confirming meeting room")

@ask.intent("DeclineMeetingRoom")
def decline_meeting():
    return statement(render_template('meeting_decline_meeting'))
    
@ask.intent("MeetingInviteSubjectIntent")
def get_meeting_subject_line(subjectLine):
    if (subjectLine):
        param["subject_meeting"] = subjectLine
        session.attributes["subjectLine"]=subjectLine
        return question(render_template('meeting_send_invite_sender_receiver'))
    else :
        return question("Kindly tell subject line ").reprompt('Kindly enter subject line')
    
@ask.intent("SenderReceiverIntent")
def set_sender_receiver(senderName,receiverName):
    senderNameValue=read_config_file(senderName)
    receiverNameValue=read_config_file(receiverName)
    print ("Vikas ####### receiverNameValue "+ receiverNameValue + "   ######## senderNameValue "+ senderNameValue)
    if(receiverNameValue != "" and senderNameValue!=""):
        receiverNameArray= receiverNameValue.split(",")
        
        #print("Vikas receiverNameArray " +receiverNameArray)
        i=0
        while i< len(receiverNameArray):
            print("Vikas receiverNameArray "+ receiverNameArray[i])
            param["to"].append(receiverNameArray[i].lstrip().rstrip())
            i+=1
        for att in param["to"] :
            print("Vikas att Vikas "+ att)
        param["from_sender"]=senderNameValue
        session.attributes["to"]=receiverNameValue
        session.attributes["from_sender"]=senderNameValue
        return question(render_template('meeting_send_invite_agenda'))
    else : 
        return statement("Sender or receivers are not registered")
    
    
@ask.intent("MeetingAgendaIntent")
def set_agenda(agenda):
    param["description"]=agenda
    session.attributes["agenda"]=agenda
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
    return (["room1","room2","room3","room4","room5","room6","room7","room8","room9","room10"])  

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
    attendees = ""
    try:
        for att in param['to']:
            print("Vikas inside loop "+att)
            #attendees += "ATTENDEE;CN="+att+";CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE;X-NUM-GUESTS=0:mailto:"+att+", "
            #attendees+=att+CRLF
        print("Vikas Attendees "+ attendees)
    except Exception as e:
        print (e)
    fro = param["from_sender"]
    
    msg = MIMEMultipart('mixed')
    msg['Reply-To']=fro
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = param["subject_meeting"]
    msg['From'] = fro
    msg['To'] = attendees
    print ("Vikas @@@@@@@@@@@@@ msg[to] ")

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    f= os.path.join(__location__, 'CalendarTemplate.ics')   
    ics_content = open(f).read()    
    description = "Hi All Kindly join the meeting the room on time. \\n\\n \\n\\n"+param["description"]+"\\n\\n \\n\\nThanks \\n\\nVikas Yadav \\n\\n"
    current_meeting_room_alias= param["locationAlias"]
    current_meeting_room=param["location"]
    currentDateTime= get_date_time()
    bookedMeetingDateStart=get_date_time_meeting_booked(param["meetingDate"],param["startTime"])
    bookedMeetingDateEnd=get_date_time_meeting_booked(param["meetingDate"],param["endTime"])
    senderName="Vikas Yadav"
    senderEmail=param["from_sender"]
    allRoomNamesAlias = ["room1Alias","room2Alias","room3Alias","room4Alias","room5Alias"]
    allRoomNamesAliasString=",".join(allRoomNamesAlias)
    htmlTextAsInviteMeeting=render_template('meeting_descrption', sender_name=senderName,meeting_agenda=param["description"])
    replace_content = {}
    try :                
        replace_content=ics_content.replace("TZID:" , "TZID:India Time Zone")        
        replace_content=replace_content.replace("TZOFFSETFROM:" , "TZOFFSETFROM:+0530")        
        replace_content=replace_content.replace("TZOFFSETTO:" , "TZOFFSETTO:+0530")        
        replace_content=replace_content.replace("ATTENDEE;CN=" , "ATTENDEE;CN=\""+current_meeting_room_alias+"\"")        
        replace_content=replace_content.replace("RSVP=TRUE:mailto:" , "RSVP=TRUE:mailto:"+current_meeting_room)        
        replace_content=replace_content.replace("CREATED:" , "CREATED:"+currentDateTime)        
        replace_content=replace_content.replace("DESCRIPTION:" , "DESCRIPTION:"+description)        
        replace_content=replace_content.replace("DTEND;TZID=" , "DTEND;TZID=\"India Time Zone\":"+bookedMeetingDateEnd)        
        replace_content=replace_content.replace("DTSTAMP:" , "DTSTAMP:"+currentDateTime)        
        replace_content=replace_content.replace("DTSTART;TZID=" , "DTSTART;TZID=\"India Time Zone\":"+bookedMeetingDateStart)        
        replace_content=replace_content.replace("LAST-MODIFIED:" , "LAST-MODIFIED:"+currentDateTime)        
        replace_content=replace_content.replace("LOCATION:" , "LOCATION:"+param["location"])        
        replace_content=replace_content.replace("ORGANIZER;CN=" , "ORGANIZER;CN=\""+senderName+"\":mailto:"+senderEmail)        
        replace_content=replace_content.replace("RESOURCES:" , "RESOURCES:"+allRoomNamesAliasString)        
        replace_content=replace_content.replace("SUMMARY;LANGUAGE=en-us:" , "SUMMARY;LANGUAGE=en-us:"+param["subject"])        
        replace_content=replace_content.replace("X-ALT-DESC;FMTTYPE=text/html:" , "X-ALT-DESC;FMTTYPE=text/html:"+htmlTextAsInviteMeeting)        
        replace_content=replace_content.replace("X-MS-OLK-APPTSEQTIME:" , "X-MS-OLK-APPTSEQTIME:"+currentDateTime)
        
        print("".join(replace_content))
        print("End #################################################################")
    except Exception as e:
        print(e)
    part_email = MIMEText(replace_content,'calendar;method=REQUEST')

    
    msgAlternative = MIMEMultipart('alternative')
   
    write_file(replace_content)
    
    ical_atch = MIMEBase('text/calendar',' ;name="%s"'%"myCalendar.ics")
    ical_atch.set_payload(replace_content)
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
    
def get_date_time():
    today=date.today()
    strDate = (str)(today)
    currentDateTime=""+strDate.split("-")[0]+strDate.split("-")[1]+strDate.split("-")[2]+"T"
    print("Vikas 1" + currentDateTime)
    currentTime =datetime.time(datetime.now())
    strTime = str(currentTime)
    currentDateTime+=strTime.split(":")[0]+strTime.split(":")[1]+(str)(math.floor((float)(strTime.split(":")[2])))+"Z"
    return currentDateTime
    print("Vikas " +currentDateTime)

def get_date_time_meeting_booked(meetingDate,meetingTime):
    meetingDate= meetingDate.split("-")
    bookedDateTime = ""+meetingDate[0]+meetingDate[1]+meetingDate[2]+"T"
    meetingTime=meetingTime.split(":")
    bookedDateTime+=meetingTime[0]+meetingTime[1]+"00Z"
    return bookedDateTime

def read_config_file(confParam):
    cfg_dict = {}
    isFound = False
    lst = []
    cfg_file = open('essconfig.cfg')
    for line in cfg_file:
        if '=' in line :
            cfg_dict[line.strip().split('=')[0]]=line.strip().split('=')[1]
        else :
            break;
    cfg_file.close()
    if confParam in cfg_dict :
        return  cfg_dict[confParam] 
    else :
        return ""          
    
    
def write_file(writeContent):
    f = open("myCalendar.ics", "w+")
    f.write(writeContent)
    f.close()
    
if __name__ == '__main__':
    app.run(debug=True)
