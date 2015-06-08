import nltk
import sys
from callapi import *


aToken='dnZhMGZ5Q3VBc2ltbGZNaFAyTWJ2UG9NMmloK1dsSFFOV0gyMTczRzhXVT0='
bId='001788fffe174db2'

print getPhilipsHueInfo(aToken, bId)

philipsControlCustom(constructCustomMsg("lights/0/state", '{"on":true}', "PUT", bId), aToken)
philipsControlCustom(constructCustomMsg("lights/1/state", '{"on":true}', "PUT", bId), aToken)
philipsControlCustom(constructCustomMsg("lights/2/state", '{"on":true}', "PUT", bId), aToken)
philipsControlCustom(constructCustomMsg("lights/3/state", '{"on":true}', "PUT", bId), aToken)
