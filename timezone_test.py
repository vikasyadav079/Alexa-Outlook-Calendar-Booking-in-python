import tzlocal;
from datetime import datetime
from datetime import date
import math

def date_time():
    today=datetime.now()
    strDate = (str)(today)
    strDate.split("-")
    print("Year is "+strDate.split("-")[1])
    print(today)
    currentTime =datetime.time(datetime.now())
    print(str(currentTime))
    strTime = str(currentTime)
   
    print(strTime.split(":")[0]+strTime.split(":")[1])
    sec = math.floor((float)(strTime.split(":")[2]))
    print(sec)
    
    
    
    
    print(today.strftime("%a,%d,%b,%y"))
    my_timezone = tzlocal.get_localzone()
    print(my_timezone)
    
def get_date_time():
    today=date.today()
    strDate = (str)(today)
    currentDateTime=""+strDate.split("-")[0]+strDate.split("-")[1]+strDate.split("-")[2]+"T"
    print("Vikas 1" + currentDateTime)
    currentTime =datetime.time(datetime.now())
    strTime = str(currentTime)
    currentDateTime+=strTime.split(":")[0]+strTime.split(":")[1]+(str)(math.floor((float)(strTime.split(":")[2])))+"Z"
    print("Vikas " +currentDateTime)
    
def get_date_time_meeting_booked(myMeetingDate,meetingTime):
    #print(meetingDate.split("-")[2])
    meetingDate=(str)(myMeetingDate)
    print(meetingDate)
       
    bookedDateTime = "{0}{1}{2}T".format(meetingDate.split("-")[0],meetingDate.split("-")[1],meetingDate.split("-")[2])
    
    bookedDateTime+=meetingTime.split(":")[0]+meetingTime.split(":")[1]+"00Z"
    print(bookedDateTime)

get_date_time_meeting_booked("2018-06-01","10:00")
