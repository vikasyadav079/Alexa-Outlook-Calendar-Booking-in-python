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
        isSenderBooked = collectionMeetingRoomDetails.find({'userName' : senderName , 'bookedDetails' : {'date' : "2018-06-01", 'startTime' : "10:30", 'endTime' : "11:00"}})
        for senderBooked in isSenderBooked :
            print(" Vikas isSenderbooked less than 0")
        else :
            print(" Vikas isSenderbooked greater than 0")

    else : 
        print ("Vikas receiverNameValue is empty")
        
 
#set_sender_receiver('vikasyadav.a079','vikasyadav079')       



def get_all_rooms():
    getAllRooms = collectionAllMeetingRooms.find();
    myRoomArray=[]
    for getRoom in getAllRooms:
        myRoomArray.append(getRoom["roomName"])
        print("Vikas get Room " + getRoom["roomName"])
    return myRoomArray 

def get_booked_rooms_db():
   print("Vikads ")
   roomArray = []
   bookedRooms = collectionMeetingRoomDetails.find({"booked": {'$elemMatch': {'date': "2018-06-01" , 'startTime' : "11:00", 'endTime' : "11:30"} }})
   for bookedRoom in bookedRooms : 
       roomArray.append(bookedRoom["roomName"])   
       print("Vikas Yadav Booked Room name " + bookedRoom["roomName"])    
   print("Vikas Yadav Booked Room name ")
   return (roomArray)
get_booked_rooms_db()
####vikasyadav079
####vikasyadav.a079
