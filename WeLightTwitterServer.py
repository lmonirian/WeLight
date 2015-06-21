import nltk
import sys
import sqlite3
import tweepy
import time
import random
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


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


# picks a random color from xy_list for each light
def setAllLightsToColorList(src, aToken, bId, xy_list):
    try:     
        jsonHueInfo = getPhilipsHueInfo(aToken, bId)
    except:
        print "Error communicating with meethue servers."
        api.send_direct_message(screen_name=src, 
            text='Error communicating with meethue servers.')
        return False          
    
    # print jsonHueInfo
    for l in jsonHueInfo["lights"]:
        philipsControlCustom(constructCustomMsg("lights/"+l+"/state", '{"on":true}', "PUT", bId), aToken)
        philipsControlCustom(constructCustomMsg("lights/"+l+"/state", '{"xy":'+random.choice(xy_list)+'}', "PUT", bId), aToken)
        philipsControlCustom(constructCustomMsg("lights/"+l+"/state", '{"bri":254}', "PUT", bId), aToken)

    return True
    
def sendDM(dest, text):
    try:
        api.send_direct_message(screen_name=dest, 
            text=text)            
    except: 
        print "ERROR: Internal error sending DM via Tweepy."    

    
# putting all color names and corresponding x,y here
wordColorList =[
    ["yellow", "[0.5, 0.44]"],
    ["blue", "[0.15, 0.08]"],
    ["green", "[0.25, 0.7]"],
    ["orange", "[0.575, 0.395]"],
    ["indigo", "[0.25, 0.02]"],
    ["violet", "[0.25, 0.02]"],
    ["red", "[0.7, 0.3]"]
]

def getColorListFromWord(text):
    cList = [];
    for t in wordColorList:
        if str.startswith(text, t[0]):
            cList.append(t[1])
    return cList
        
def processLightCommand(dest, src, text):
    print "Processing light command from "+src+" to "+dest+":"+text
    # todo: replace code below with NLTK code to parse light command
    if checkPermission(src, dest):
        (t, b) = getTokenAndBridgeId(dest)
        tokens = nltk.word_tokenize(text)
        tagged = nltk.pos_tag(tokens)
        colorList = []
        for tuple in tagged:
            print tuple
            colorList = colorList + getColorListFromWord(tuple[0])
        
        if colorList == []:
            sendDM(src, 'Could not identify any colors from sentence')
            return
            
        if setAllLightsToColorList(src, t, b, colorList):    		   		
            sendDM(src, 'Successfully sent light message to '+dest)    
    else:
        sendDM(src, 'You are not authorized to send light messages to '+dest)  

def processDMCommand(dm):
    src = dm['sender_screen_name']
    msg_text = dm['text'].encode("utf-8")
    command_and_parms = msg_text.split(' ', 1 );
    command = command_and_parms[0]


    # light command to a user: @<dest> light command
    if str.startswith(command, "@"):
        processLightCommand(str.lstrip(command, "@"), src, command_and_parms[1])
        return

    # command to add new access token: _signup <token> <bridgeId>
    if str.startswith(command, "_signup"):
        # spliiting rest of parameters
        parms = command_and_parms[1].split(' ', 1 );
        newToken = parms[0]
        newbId = parms[1]
        print "Signing up new user:"+ src+" b:"+newbId+" t:"+newToken
        c = conn.cursor()
        c.execute("insert or replace into usertokens values ('"+src+"','"+newbId+"','"+newToken+"')")        
        c.execute("insert into userperms values ('"+src+"','"+src+"')")
        conn.commit()
        sendDM(src, 'Successfully updated token and bridge for ' + src)
        return
        
    # command to authorize user: _auth @user
    if str.startswith(command, "_auth"):
        newSrcUser = command_and_parms[1]
        print "New authorization:"+ src + " <- " + newSrcUser
        c = conn.cursor()
        c.execute("insert into userperms values ('"+src+"','"+newSrcUser+"')")
        sendDM(src, 'Successfully authorized ' + newSrcUser + ' to send light messages to ' + src)
        conn.commit()
        return

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        print "Tweet:"
        print(data)
        datadict = json.loads(data)

        if 'direct_message' in data:
            # print datadict
            dm = datadict['direct_message']
            print "DM:"
            print "(" + str(dm['id']) + ") " + dm['sender_screen_name'] +" : "+ dm['text']
            processDMCommand(dm)
        
        if 'event' in data:
            if datadict['event'] == 'follow':
                newfollower = datadict['source']['screen_name']
                if newfollower != 'we_Light_':
                    print "New follower: " + newfollower
                    api.create_friendship(screen_name=newfollower)
                    sendDM(newfollower, 'Welcome to WeLight! To signup DM: _signup <token> <bridgeId>')
                    sendDM(newfollower, 'To authorize an user DM: _auth <screen name>')
                    sendDM(newfollower, 'To send a light command DM: @<screen name> <command in natural english, e.g. yellow>')
        
    def on_error(self, status):
        print "Error:"
        print(status)
        
        

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

print "Check for followers and automatically add them."
for follower in tweepy.Cursor(api.followers).items():
    print follower.screen_name
    follower.follow()


l = StdOutListener()
stream = Stream(auth, l)
stream.userstream()
