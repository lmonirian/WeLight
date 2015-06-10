import nltk
import sys
import sqlite3

from callapi import *


# lab
# aToken='dnZhMGZ5Q3VBc2ltbGZNaFAyTWJ2UG9NMmloK1dsSFFOV0gyMTczRzhXVT0='
# bId='001788fffe174db2'

# home
# aToken='MWRuUkdndGVUc2VnTjJIZW1FWXVzOFYxZmFFNUlWNFlQOTB4VllmSlkxTT0='
# bId='001788fffe17b990'

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


srcUser = "we_Light_"
destUser = "luisceze"

if checkPermission(srcUser, destUser):
    (t, b) = getTokenAndBridgeId(destUser)    
    setAllLightsToColor(t, b, "[0.32,0.1]")

