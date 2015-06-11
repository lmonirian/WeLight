import nltk
import sys
import sqlite3
import tweepy
import time

from callapi import *

conn = sqlite3.connect('db/welight.db')

def getTokenAndBridgeId(username):
    c = conn.cursor()
    c.execute("select * from usertokens where userhandle like'"+username+"'")
    row = c.fetchone()

    if row == None:
        return ("","")
    
    return (row[2],row[1])

def checkPermission(userFrom, userTo):
    c = conn.cursor()
    c.execute("select * from userperms where dest='"+userTo+"' and src='"+userFrom+"'")
    row = c.fetchone()

    if row == None:
        return False
    return True

def setAllLightsToColor(aToken, bId, xy):
    jsonHueInfo = getPhilipsHueInfo(t, b)
    print jsonHueInfo
    for l in jsonHueInfo["lights"]:
        philipsControlCustom(constructCustomMsg("lights/"+l+"/state", '{"on":true}', "PUT", bId), aToken)
        philipsControlCustom(constructCustomMsg("lights/"+l+"/state", '{"xy":'+xy+'}', "PUT", bId), aToken)


# srcUser = "we_Light_"
# destUser = "luisceze"
# if checkPermission(srcUser, destUser):
#     (t, b) = getTokenAndBridgeId(destUser)
#     setAllLightsToColor(t, b, "[0.32,0.1]")


# monitoring the twitter account for direct messages
auth = tweepy.OAuthHandler("IFOyuJtAPeXV5J0Gd0ahomBlA", "izvHwkSJhPpmr0IakpFOFwvs44svrj5rWZ56h1nSrSbqLsNg4N")
auth.set_access_token("3235468296-2TzMkX6CASeJ8GTBcCIoHOT8PUuD5Zq9FknSwSG", "OuRQFa8yblPS9whaEmxS0cMVowIYWzCtpehxTmx1mCXmM")

api = tweepy.API(auth)
direct_messages = api.direct_messages()

highest_dm_id = 0

print "Old messages:"
for dm in direct_messages:
    print "(" + str(dm.id) + ") " + dm.sender_screen_name +" : "+ dm.text
    if dm.id > highest_dm_id:
        highest_dm_id = dm.id

print "New messages:"

while True:
    direct_messages = api.direct_messages(highest_dm_id)
    for dm in direct_messages:
        print "(" + str(dm.id) + ") " + dm.sender_screen_name +" : "+ dm.text
        # todo process light command here. 
        if dm.id > highest_dm_id:
            highest_dm_id = dm.id
    time.sleep(60)
    

