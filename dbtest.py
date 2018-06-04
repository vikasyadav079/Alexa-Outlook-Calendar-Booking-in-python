'''
Created on May 24, 2018

@author: vikasy
'''
import pymongo
import pprint

from pymongo import MongoClient, collection
client = MongoClient()
client = MongoClient('mongodb://localhost:27017/')
db = client.meetingrooms
collection = db.meetingRoomDetails


try :
    bookedRoomsDetails = collection.find({"booked": {'$elemMatch': {'date': '2018-05-25' , 'startTime' : '15:30', 'endTime' : '16:30'} }})
       
    for posts in bookedRoomsDetails :
        pprint.pprint(posts)
    print("Rows fetched ")

except Exception  as  e :
    print (e)
    
    #bookedRoomsDetails =  collection.find({'$not':[{'availableSlots': {'$elemMatch': {'startTime':startTime , 'endTime':endTime, 'isAvailable' : 0}}}]})