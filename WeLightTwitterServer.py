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
		sendDM(src, 'Error communicating with meethue servers.')
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
		try: 
			api.send_direct_message(screen_name=dest, 
	            text=text)            
		except:
			print "ERROR: Internal error sending DM via Tweepy."    

    
# putting all color names and corresponding x,y here
wordColorList =[
    ["yellow", "[0.4432, 0.5154]"],
    ["blue", "[0.139, 0.081]"],
    ["green", "[0.214, 0.709]"],
    ["orange", "[0.5614, 0.4156]"],
    ["indigo", "[0.2332, 0.1169]"],
    ["violet", "[0.3644, 0.2133]"],
    ["red", "[0.675, 0.322]"],
    ["white", "[0.3227, 0.329]"],
    ["lime", "[0.5, 0.475]"],
    ["light blue", "[0.2621, 0.3157]"],
    ["pink", "[0.5, 0.24]"],
    ["cyan", "[0.17, 0.3403]"],
    ["magenta", "[0.3787, 0.1724]"],
    ["periwinkle", "[0.17, 0.0]"],
    ["turqouise", "[0.1732, 0.3672]"],
    ["light emerald", "[0.3, 0.555]"],
    ["fuschia", "[0.3787, 0.1724]"],
    ["royal blue", "[0.1649, 0.1338]"],
    ["cobalt", "[0.2, 0.23]"],
    ["ocean", "[0.035, 0.38]"],
    ["plum", "[0.3495, 0.2545]"],
    ["honey", "[0.545, 0.415]"],
    ["pickle", "[0.145, 0.715]"],
    ["basil", "[0.08, 0.545]"],
    ["alice blue", "[0.3088, 0.3212]"],
    ["antique white", "[0.3548, 0.3489]"],
    ["aqua", "[0.17, 0.3403]"],
    ["aquamarine", "[0.2138, 0.4051]"],
    ["azure", "[0.3059, 0.3303]"],
    ["beige", "[0.3402, 0.356]"],
    ["bisque", "[0.3806, 0.3576]"],
    ["black", "[[0.139, 0.081]"],
    ["blanched almond", "[0.3695, 0.3584]"],
    ["blue violet", "[0.245, 0.1214]"],
    ["brown", "[0.6399, 0.3041]"],
    ["burlywood", "[0.4236, 0.3811]"],
    ["cadet blue", "[0.2211, 0.3328]"],
    ["chartreuse", "[0.2682, 0.6632]"],
    ["chocolate", "[0.6009, 0.3684]"],
    ["coral", "[0.5763, 0.3486]"],
    ["cornflower", "[0.1905, 0.1945]"],
    ["cornsilk", "[0.3511, 0.3574]"],
    ["crimson", "[0.6531, 0.2834]"],
    ["dark blue", "[0.139, 0.081]"],
    ["dark cyan", "[0.17, 0.3403]"],
    ["dark goldenrod", "[0.5265, 0.4428]"],
    ["dark green", "[0.214, 0.709]"],
    ["dark khaki", "[0.4004, 0.4331]"],
    ["dark magenta", "[0.3787, 0.1724]"],
    ["dark olive green", "[0.3475, 0.5047]"],
    ["dark orange", "[0.5951, 0.3872]"],
    ["dark orchid", "[0.296, 0.1409]"],
    ["dark red", "[0.7, 0.2986]"],
    ["dark salmon", "[0.4837, 0.3479]"],
    ["dark sea green", "[0.2924, 0.4134]"],
    ["dark slate blue", "[0.2206, 0.1484]"],
    ["dark slate gray", "[0.2239, 0.3368]"],
    ["dark turquoise", "[0.1693, 0.3347]"],
    ["dark violet", "[0.2742, 0.1326]"],
    ["deep pink", "[0.5454, 0.2359]"],
    ["deep sky blue", "[0.1576, 0.2368]"],
    ["dim gray", "[0.3227, 0.329]"],
    ["dodger blue", "[0.1484, 0.1599]"],
    ["firebrick", "[0.1484, 0.1599]"],
    ["floral white", "[0.3361, 0.3388]"],
    ["gainsboro", "[0.3227, 0.329]"],
    ["ghost white", "[0.3174, 0.3207]"],
    ["gold", "[0.4947, 0.472]"],
    ["goldenrod", "[0.5136, 0.4444]"],
    ["gray", "[0.3227, 0.329]"],
    ["web gray", "[0.3227, 0.329]"],
    ["web green", "[0.214, 0.709]"],
    ["green yellow", "[0.3298, 0.5959]"],
    ["honeydew", "[0.316, 0.3477]"],
    ["hot pink", "[0.4682, 0.2452]"],
    ["indian red", "[0.5488, 0.3112]"],
    ["ivory", "[0.3334, 0.3455]"],
    ["khaki", "[0.4019, 0.4261]"],
    ["lavender", "[0.3085, 0.3071]"],
    ["lavender blush", "[0.3369, 0.3225]"],
    ["lawn green", "[0.2663, 0.6649]"],
    ["lemon chiffon", "[0.3608, 0.3756]"],
    ["light coral", "[0.5075, 0.3145]"],
    ["light cyan", "[0.2901, 0.3316]"],
    ["light goldenrod", "[0.3504, 0.3717]"],
    ["light gray", "[0.3227, 0.329]"],
    ["light green", "[0.2648, 0.4901]"],
    ["light pink", "[0.4112, 0.3091]"],
    ["light salmon", "[0.5016, 0.3531]"],
    ["light sea green", "[0.1721, 0.358]"],
    ["light sky blue", "[0.214, 0.2749]"],
    ["light slate gray", "[0.2738, 0.297]"],
    ["light steel blue", "[0.276, 0.2975]"],
    ["light yellow", "[0.3436, 0.3612]"],
    ["lime", "[0.214, 0.709]"],
    ["lime green", "[0.2101, 0.6765]"],
    ["linen", "[0.3411, 0.3387]"],
    ["maroon", "[0.5383, 0.2566]"],
    ["web maroon", "[0.7, 0.2986]"],
    ["medium aquamarine", "[0.215, 0.4014]"],
    ["medium blue", "[0.139, 0.081]"],
    ["medium orchid", "[0.3365, 0.1735]"],
    ["medium purple", "[0.263, 0.1773]"],
    ["medium sea green", "[0.1979, 0.5005]"],
    ["medium slate blue", "[0.2179, 0.1424]"],
    ["medium spring green", "[0.1919, 0.524]"],
    ["medium turquoise", "[0.176, 0.3496]"],
    ["medium violet red", "[0.504, 0.2201]"],
    ["midnight blue", "[0.1585, 0.0884]"],
    ["mint cream", "[0.315, 0.3363]"],
    ["misty rose", "[0.3581, 0.3284]"],
    ["moccasin", "[0.3927, 0.3732]"],
    ["navajo white", "[0.4027, 0.3757]"],
    ["navy blue", "[0.139, 0.081]"],
    ["old lace", "[0.3421, 0.344]"],
    ["olive", "[0.4432, 0.5154]"],
    ["olive drab", "[0.354, 0.5561]"],
    ["orange red", "[0.6726, 0.3217]"],
    ["orchid", "[0.3688, 0.2095]"],
    ["pale goldenrod", "[0.3751, 0.3983]"],
    ["pale green", "[0.2675, 0.4826]"],
    ["pale turqoise", "[0.2539, 0.3344]"],
    ["pale violet red", "[0.4658, 0.2773]"],
    ["papaya whip", "[0.3591, 0.3536]"],
    ["peach puff", "[0.3953, 0.3564]"],
    ["peru", "[0.5305, 0.3911]"],
    ["pink", "[0.3944, 0.3093]"],
    ["powder blue", "[0.262, 0.3269]"],
    ["purple", "[0.2651, 0.1291]"],
    ["web purple", "[0.3787, 0.1724]"],
    ["rebecca purple", "[0.2703, 0.1398]"],
    ["rosy brown", "[0.4026, 0.3227]"],
    ["saddle brown", "[0.5993, 0.369]"],
    ["salmon", "[0.5346, 0.3247]"],
    ["sandy brown", "[0.5104, 0.3826]"],
    ["sea green", "[0.1968, 0.5047]"],
    ["seashell", "[0.3397, 0.3353]"],
    ["sienna", "[0.5714, 0.3559]"],
    ["silver", "[0.3227, 0.329]"],
    ["slate blue", "[0.2218, 0.1444]"],
    ["slate gray", "[0.2762, 0.3009]"],
    ["snow", "[0.3292, 0.3285]"],
    ["spring green", "[0.1994, 0.5864]"],
    ["steel blue", "[0.183, 0.2325]"],
    ["tan", "[0.4035, 0.3772]"],
    ["teal", "[0.17, 0.3403]"],
    ["thistle", "[0.3342, 0.2971]"],
    ["tomato", "[0.6112, 0.3261]"],
    ["wheat", "[0.3852, 0.3737]"],
    ["white smoke", "[0.3227, 0.329]"],
    ["yellow green", "[0.3517, 0.5618]"],
    ##start of analogies
    ["forest", "[0.2097, 0.6732]"],
    ["sky", "[0.2206, 0.2948]"],
    ["sun", "[0.56, 0.445]"],
    ["storm", "[0.3227, 0.329]"]
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
            sendDM(src, 'Could not identify any colors from sentence, picking a random one.')
            colorList = colorList + random.choice(wordColorList)
            
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

        if 'direct_message' in datadict:
            # print datadict
            dm = datadict['direct_message']
            print "DM:"
            print "(" + str(dm['id']) + ") " + dm['sender_screen_name'] +" : "+ dm['text']
            processDMCommand(dm)
        
        if 'event' in datadict:
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
