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
    jsonHueInfo = getPhilipsHueInfo(aToken, bId)
    print jsonHueInfo
    for l in jsonHueInfo["lights"]:
        philipsControlCustom(constructCustomMsg("lights/"+l+"/state", '{"on":true}', "PUT", bId), aToken)
        philipsControlCustom(constructCustomMsg("lights/"+l+"/state", '{"xy":'+xy+'}', "PUT", bId), aToken)

def processLightCommand(dest, src, text):
    print "Processing light command from "+src+" to "+dest+":"+text
    # todo: replace code below with NLTK code to parse light command
    if checkPermission(src, dest):
        (t, b) = getTokenAndBridgeId(dest)
        setAllLightsToColor(t, b, "[0.32,0.1]")

def processDMCommand(dm):
    src = dm.sender_screen_name
    msg_text = dm.text.encode("utf-8")
    command_and_parms = msg_text.split(' ', 1 );
    command = command_and_parms[0]


    # light command to a user: @<dest> light command
    if str.startswith(command, "@"):
        processLightCommand(str.lstrip(command, "@"), src, command_and_parms[1])
        return

    # command to add new access token: __token <token> <bridgeId>
    if str.startswith(command, "__signup"):
        # spliiting rest of parameters
        parms = command_and_parms[1].split(' ', 1 );
        newToken = parms[0]
        newbId = parms[1]
        print "Signing up new user:"+ src+" b:"+newbId+" t:"+newToken
        c = conn.cursor()
        c.execute("insert into usertokens values ('"+src+"','"+newbId+"','"+newToken+"')")
        conn.commit()
        return
        
    # command to authorize user: __auth @user
    if str.startswith(command, "__auth"):
        newSrcUser = command_and_parms[1]
        print "New authorization:"+ src + " <- " + newSrcUser
        c = conn.cursor()
        c.execute("insert into userperms values ('"+src+"','"+newSrcUser+"')")
        conn.commit()
        return

# twitter oAuth
auth = tweepy.OAuthHandler("IFOyuJtAPeXV5J0Gd0ahomBlA", "izvHwkSJhPpmr0IakpFOFwvs44svrj5rWZ56h1nSrSbqLsNg4N")
auth.set_access_token("3235468296-2TzMkX6CASeJ8GTBcCIoHOT8PUuD5Zq9FknSwSG", "OuRQFa8yblPS9whaEmxS0cMVowIYWzCtpehxTmx1mCXmM")
api = tweepy.API(auth)


highest_dm_id = 0
print "Old messages:"
for dm in api.direct_messages():
    print "(" + str(dm.id) + ") " + dm.sender_screen_name +" : "+ dm.text
    if dm.id > highest_dm_id:
        highest_dm_id = dm.id

timer = 0
print "New messages:"
while True:
    for dm in api.direct_messages(highest_dm_id):
        print "(" + str(dm.id) + ") " + dm.sender_screen_name +" : "+ dm.text
        processDMCommand(dm)
        if dm.id > highest_dm_id:
            highest_dm_id = dm.id
    
    if (timer % 10) == 0:
        print "Checking for followers and automatically add them."
    for follower in tweepy.Cursor(api.followers).items():
        follower.follow()
    
    time.sleep(60) # wait 60 seconds --- Twitter does rate limiting (i think at 15 reqs per minute)
    timer = timer + 1
    
