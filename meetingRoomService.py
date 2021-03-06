import logging
import pprint
import threading

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
collectionMeetingRoomDetails = db.meetingRoomDetails
collectionUserMeetingScheduledDetails = db.userMeetingScheduledDetails
collectionAllMeetingRooms=db.allMeetingRooms
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

threads=[]


@ask.launch
def launched ():
    print(render_template('meeting_descrption',meeting_agenda="VikasYadavAgent",sender_name="VikasYadavSenderNAme"))
    return question(render_template('meeting_welcome')).reprompt(render_template('meeting_welcome_prompt'))

@ask.intent("AMAZON.FallbackIntent")
@ask.intent("AMAZON.CancelIntent")
@ask.intent("AMAZON.StopIntent")
def meeting_skill_cancel():
    return statement (render_template('meeting_invite_cancel'))


@ask.intent("AMAZON.HelpIntent")
def help_intent():
    print ("Vikasy helpIntent has been called......................................")
    return statement("Thanks for using Alexa for meeting invitation")

@ask.intent("CheckMeetingRoomsIntent")
def check_meeting_rooms(meetingDate, startTime, endTime):
    print("Vikasy meeting Date : %s startTime : %s endTime : %s " % (meetingDate, startTime, endTime))
    ######## query db 
    booked_rooms =  get_booked_rooms_db(meetingDate, startTime, endTime)
    session.attributes["startTime"]=startTime
    session.attributes["endTime"]=endTime
    session.attributes["meetingDate"]=meetingDate
    all_rooms = get_all_rooms()
    available_rooms=[]
    if len(all_rooms)>0:
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
            return statement("No meeting rooms are availbale for now. Thanks for using calling ")
    else:
        return statement("No meeting rooms are availbale for now. Thanks for using calling ")

@ask.intent("CheckOneMeetingRoomIntent")
def check_one_meeting_room(meetingRoom,meetingDate,startTime,endTime):
    if get_single_room_status(meetingRoom,meetingDate,startTime,endTime) :
        session.attributes["startTime"]=startTime
        session.attributes["endTime"]=endTime
        session.attributes["meetingDate"]=meetingDate
        session.attributes["meetingRoomInContext"]=meetingRoom
        session.attributes["meetingRoom"]=meetingRoom
        session.attributes["isAvailable"]=True
        return question(render_template('meeting_check_meeting_room_single_success', meeting_room='meetingRoom',meeting_date='meetingDate',start_time='startTime',end_time='endTime')).reprompt(render_template('meeting_confirm_meeting_prompt'))
    else :
        session.attributes["startTime"]=""
        session.attributes["endTime"]=""
        session.attributes["meetingDate"]=""
        session.attributes["meetingRoomInContext"]=meetingRoom
        session.attributes["meetingRoom"]=""
        session.attributes["isAvailable"]=False
        return question(render_template('meeting_check_meeting_room_single_fail'))
    
    
@ask.intent("ConfirmMeetingRoomInContext")
def confirmation_single_room_message():  
    if (session.attributes["isAvailable"]) :  
        param["startTime"]=session.attributes["startTime"]
        param["endTime"]=session.attributes["endTime"]
        meetingRoomValue=read_config_file(session.attributes["meetingRoomInContext"])
        meetingRoomValueAlias=read_config_file(session.attributes["meetingRoomInContext"])
        param["meetingDate"]=session.attributes["meetingDate"]
        param["location"]=meetingRoomValue
        param["locationAlias"]=meetingRoomValueAlias+"Vikas"
        return question(render_template('meeting_send_invite_sender_receiver'))#
    else:
        param["startTime"]=""
        param["endTime"]=""
        param["meetingDate"]=""
        param["location"]=""
        param["locationAlias"]=""
        return question("Sorry this room is already booked. Kindly select another room ")

@ask.intent("ConfirmMeetingRoomIntent")
def confirmation_message(meetingRoom):
    for att in session.attributes["available_rooms"]: 
        print("Vikas meeting room in session "+ att)
    if meetingRoom in session.attributes["available_rooms"] :
        param["startTime"]=session.attributes["startTime"]
        param["endTime"]=session.attributes["endTime"]
        param["meetingDate"]=session.attributes["meetingDate"]
        #meetingRoomValue=read_config_file(meetingRoom)
        meetingRoomValueAlias=''
        print("Vikas "+meetingRoom.lstrip().rstrip()+"Alias")
        meetingRoomValueAlias=read_config_file((meetingRoom.lstrip().rstrip()+"Alias"))
        print("Vikas Yadabv " + meetingRoomValueAlias)
        if meetingRoomValueAlias!='':
            param["location"]=meetingRoom
            param["locationAlias"]=meetingRoomValueAlias
            return question(render_template('meeting_send_invite_sender_receiver'))#
        else:
            return statement("Problem with skill. While confirming meeting room")
    else : 
        param["startTime"]=""
        param["endTime"]=""
        param["meetingDate"]=""
        param["location"]=""
        param["locationAlias"]=""
        return question("This meeting room is already booked. Kindly select another room")

@ask.intent("DeclineMeetingRoom")
def decline_meeting():
    return statement(render_template('meeting_decline_meeting'))


@ask.intent("SuccessConfirmMeetingAfterCollisionIntent")   
@ask.intent("MeetingInviteSubjectIntent")
def get_meeting_subject_line(subjectLine):
    if (subjectLine):
        param["subject_meeting"] = subjectLine
        session.attributes["subjectLine"]=subjectLine
        return question(render_template('meeting_send_invite_agenda'))#meeting_confirm_meeting
    else :
        param["subject_meeting"] =""
        session.attributes["subjectLine"]=""
        return question("Kindly tell subject line ").reprompt('Kindly enter subject line')
    
@ask.intent("SenderReceiverIntent")
def set_sender_receiver(senderName,receiverName):
    senderNameValue=read_config_file(senderName)
    receiverNameValue=read_config_file(receiverName)
    if(receiverNameValue != "" and senderNameValue!=""):
        receiverNameArray= receiverNameValue.split(",")
        i=0
        while i< len(receiverNameArray):
            param["to"].append(receiverNameArray[i].lstrip().rstrip())
            i+=1
        param["from_sender"]=senderNameValue
        isSenderBooked={}
        isSenderBooked = collectionMeetingRoomDetails.find({'userName' : senderName , 'bookedDetails' : {'date' : session.attributes["meetingDate"], 'startTime' : session.attributes["startTime"], 'endTime' : session.attributes["endTime"]}})
        count=0
        for senderBooked in isSenderBooked:
            count+=1;
        if count > 0 :
            return question("This meeting room is already colliding with other meeting room. Would you like to book this meeting instead ? ")
        else :
            session.attributes["to"]=param["to"]
            session.attributes["from_sender"]=senderNameValue
            return question(render_template('meeting_confirm_meeting'))
    else : 
        param["from_sender"]=""
        param["to"]=[]
        session.attributes["to"]=[]
        session.attributes["from_sender"]=""
        return statement("Sender or receivers are not registered")
    
  
@ask.intent("MeetingAgendaIntent")
def set_agenda(agenda):
    param["description"]=agenda
    session.attributes["agenda"]=agenda
    #collectionMeetingRoomDetails.insert({'roomName' : param["location"], 'booked' :{'date' : param["meetingDate"], 'startTime' : param["startTime"], 'endTime':param["endTime"]}})
    #t1 = threading.Thread(target=set_meeting_booking())
    print("Vikas Meeting Agenda Intent")
    return statement (render_template('meeting_sent_invite'))
    #t2 = threading.Thread(target=send_invite(),arg=(param))
    #t1.start()
    #t2.start()
    #set_user_calendar()
    #set_meeting_booking()
    #send_invite(param)
    


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
    
def get_booked_rooms_db(bookedDates, startTime, endTime ):
   roomArray = []
   bookedRooms = collectionMeetingRoomDetails.find({"booked": {'$elemMatch': {'date': bookedDates , 'startTime' : startTime, 'endTime' : endTime} }})
   for bookedRoom in bookedRooms : 
       roomArray.append(bookedRoom["roomName"])   
       print("Vikas Yadav Booked Room name " + bookedRoom["roomName"])    
   return (roomArray)

def get_all_rooms():
    getAllRooms = collectionAllMeetingRooms.find();
    myRoomArray=[]
    for getRoom in getAllRooms:
        myRoomArray.append(getRoom["roomName"])
    return myRoomArray  

def get_single_room_status(roomName,bookedDates,startTime,endTime):
    #bookedRooms = collectionMeetingRoomDetails.count({'$and':{{'roomName' : roomName },{"booked": {'$elemMatch': {'date': bookedDates , 'startTime' : startTime, 'endTime' : endTime}}} }})
    bookedRooms = collectionMeetingRoomDetails.count({'roomName' : roomName, "booked": {'$elemMatch': {'date': bookedDates, 'startTime' : startTime, 'endTime' : endTime}}})
    if bookedRooms :
        return (1)
    else :
        return (0)  

def set_meeting_booking():
    if param["location"] in session.attributes["available_rooms"]:
        print("Vikas Updating location in db ")
        collectionMeetingRoomDetails.update({'roomName' : param["location"] },{'$push': {'booked' : {'date': param["meetingDate"] , 'startTime' : param["startTime"], 'endTime' : param["endTime"]}}})
    else:
        print("Vikas inserting location in db ")
        collectionMeetingRoomDetails.insert({'roomName' : param["location"], 'booked' :{'date' : param["meetingDate"], 'startTime' : param["startTime"], 'endTime':param["endTime"]}})
    return

def set_user_calendar():
    for userId in param["to"] :
        count = 0
        count = collectionUserMeetingScheduledDetails.count({'userName' : userId})
        if count > 0 :
            ##upgrade query
            print("Vikas updating user calendar") 
            collectionUserMeetingScheduledDetails.update({'userName' : userId},{'$push' : {'bookedDetails' : {'date': param["meetingDate"] , 'startTime' : param["startTime"], 'endTime' : param["endTime"]}}})
        else : 
            print("Vikas inserting user calendar") 
            collectionUserMeetingScheduledDetails.insert({'userName' : userId, 'bookedDetails' : [{'date': param["meetingDate"] , 'startTime' : param["startTime"], 'endTime' : param["endTime"]}]})
            

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
            attendees+=att+CRLF
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

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    f= os.path.join(__location__, 'myCalendar.ics')  
    
    senderName=read_config_file((param["from_sender"].lstrip().rstrip()+"Name"))
    description = "Hi All Kindly join the meeting the room on time. \\n\\n \\n\\n"+param["description"]+"\\n\\n \\n\\nThanks \\n\\n"+senderName+"\\n\\n"
    current_meeting_room_alias= param["locationAlias"]
    current_meeting_room=param["location"]
    currentDateTime= get_date_time()
    bookedMeetingDateStart=get_date_time_meeting_booked(param["meetingDate"],param["startTime"])
    bookedMeetingDateEnd=get_date_time_meeting_booked(param["meetingDate"],param["endTime"])
    
    senderEmail=param["from_sender"]
    allRoomNamesAlias=[]
    for rooms in session.attributes["all_rooms"]:
        allRoomNamesAlias.append(read_config_file((rooms.lstrip().rstrip()+"Alias")))
    allRoomNamesAliasString=", ".join(allRoomNamesAlias)
    print("Vikas " + allRoomNamesAliasString)
    htmlTextAsInviteMeeting=render_template('meeting_descrption', sender_name=senderName,meeting_agenda=param["description"])
    generate_contents = ""
    try :                
        CRLF="\r\n" 
        generate_contents+="BEGIN:VCALENDAR"+CRLF     
        generate_contents+="PRODID:-//Microsoft Corporation//Outlook 16.0 MIMEDIR//EN"+CRLF
        generate_contents+="VERSION:2.0"+CRLF
        generate_contents+="METHOD:REQUEST"+CRLF
        generate_contents+="X-MS-OLK-FORCEINSPECTOROPEN:TRUE"+CRLF
        generate_contents+="BEGIN:VTIMEZONE"+CRLF
        generate_contents+="TZID:India Standard Time"+CRLF
        generate_contents+="BEGIN:STANDARD"+CRLF
        generate_contents+="DTSTART:16010101T000000"+CRLF
        generate_contents+="TZOFFSETFROM:+0000"+CRLF
        generate_contents+="TZOFFSETTO:+0000"+CRLF
        generate_contents+="END:STANDARD"+CRLF
        generate_contents+="END:VTIMEZONE"+CRLF
        generate_contents+="BEGIN:VEVENT"+CRLF
        generate_contents+="ATTENDEE;CN="+current_meeting_room_alias+";CUTYPE=RESOURCE;ROLE=NON-PARTICIPANT;RSVP=TRUE:mailto:"+current_meeting_room+CRLF
        for att in param['to']:
            generate_contents+="ATTENDEE;CN="+att+";RSVP=TRUE:mailto:"+att+CRLF        
        generate_contents+="CLASS:PUBLIC"+CRLF
        generate_contents+="CREATED:"+currentDateTime+CRLF
        generate_contents+="DESCRIPTION:"+description+CRLF
        generate_contents+="DTEND;TZID=\"India Standard Time\":"+bookedMeetingDateEnd+CRLF
        generate_contents+="DTSTAMP:"+currentDateTime+CRLF
        generate_contents+="DTSTART;TZID=\"India Standard Time\":"+bookedMeetingDateStart+CRLF
        generate_contents+="LAST-MODIFIED:"+currentDateTime+CRLF
        generate_contents+="LOCATION:"+current_meeting_room_alias+CRLF
        generate_contents+='ORGANIZER;CN=\"'+senderName+'\":mailto:'+senderEmail+CRLF
        generate_contents+="PRIORITY:5"+CRLF
        generate_contents+="RESOURCES:"+allRoomNamesAliasString+CRLF
        generate_contents+="SEQUENCE:0"+CRLF
        generate_contents+="SUMMARY;LANGUAGE=en-us:"+param["description"]+CRLF
        generate_contents+="TRANSP:OPAQUE"+CRLF
        generate_contents+="UID:040000008200E00074C5B7101A82E00800000000703FC36ECDF8D301000000000000000010000000AB63908CFB151A4BB215A64723BAC267"+CRLF
        generate_contents+="X-ALT-DESC;FMTTYPE=text/html:"+htmlTextAsInviteMeeting+CRLF
        generate_contents+="X-MICROSOFT-CDO-BUSYSTATUS:BUSY"+CRLF
        generate_contents+="X-MICROSOFT-CDO-IMPORTANCE:1"+CRLF
        generate_contents+="X-MICROSOFT-DISALLOW-COUNTER:FALSE"+CRLF
        generate_contents+="X-MS-OLK-APPTSEQTIME:"+currentDateTime+CRLF
        generate_contents+="X-MS-OLK-AUTOFILLLOCATION:TRUE"+CRLF
        generate_contents+="X-MS-OLK-CONFTYPE:0"+CRLF
        generate_contents+="EGIN:VALARM"+CRLF
        generate_contents+="TRIGGER:-PT15M"+CRLF
        generate_contents+="ACTION:DISPLAY"+CRLF
        generate_contents+="DESCRIPTION:Reminder"+CRLF
        generate_contents+="END:VALARM"+CRLF
        generate_contents+="END:VEVENT"+CRLF
        generate_contents+="END:VCALENDAR"+CRLF
        print("End #################################################################")
    except Exception as e:
        print(e)
    part_email = MIMEText(generate_contents,'calendar;method=REQUEST')

    
    msgAlternative = MIMEMultipart('alternative')
   
    write_file(generate_contents)
    
    ical_atch = MIMEBase('text/calendar',' ;name="%s"'%"myCalendar.ics")
    ical_atch.set_payload(generate_contents)
    encoders.encode_base64(ical_atch)
    ical_atch.add_header('Content-Disposition', 'attachment; filename="myCalendar.ics"')
    

    
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
    currentTime =datetime.time(datetime.now())
    strTime = str(currentTime)
    currentDateTime+=strTime.split(":")[0]+strTime.split(":")[1]+(str)(math.floor((float)(strTime.split(":")[2])))+"Z"
    return currentDateTime

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
