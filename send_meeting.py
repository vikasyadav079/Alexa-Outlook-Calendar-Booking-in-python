import smtplib

from email.utils import formatdate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

from email import encoders
import os, datetime
from asn1crypto._ffi import null


from datetime import datetime
from datetime import date
import math

from flask import render_template

param = {
    "to": "vikasyadav079@outlook.com",
    "subject": "Party reminder",
    "location": "Koramangala 5th Block, Bangalore",
    "description": "Hangout",
    "meetingStartDate": "20150512T083000Z",
    "meetingEndDate": "20150512T093000Z",
    "agenda" : "This is my agenda "
    }


def send_meeting():
    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    f= os.path.join(__location__, 'CalendarTemplate.ics')   
    ics_content = open(f).read()
    
    description = "Hi All Kindly join the meeting the room on time. \\n\\n \\n\\nIts regarding testing Angular 2.\\n\\n \\n\\nThanks \\n\\nVikas Yadav \\n\\n"
    current_meeting_room_alias= "^Ind_Magarpatta_T6_BU_ Saphire_Big_Meeting_Room (VC)"
    current_meeting_room="TowerVIBUSaphire@Amdocs.com"
    currentDateTime= get_date_time()
    bookedMeetingDateStart=get_date_time_meeting_booked("2018-06-01","10:00")
    bookedMeetingDateEnd=get_date_time_meeting_booked("2018-06-01","11:00")
    senderName="Vikas Yadav"
    senderEmail="Vikas.Yadav@admocs.com"
    allRoomNamesAlias = ["Room1Alias","Room2Alias","Room3Alias","Room4Alias","Room5Alias",]
    allRoomNamesAliasString=",".join(allRoomNamesAlias)
    #htmlTextAsInviteMeeting=render_template('descriptionTemplate.yaml', sender_name=senderName,meeting_agenda=param["agenda"])
    htmlTextAsInviteMeeting="Hey there white cow"
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
       
     #
       
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
    
send_meeting()
    