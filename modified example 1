#!/usr/bin/python

import sys
sys.path.append('/Users/lydiamonirian/Desktop/phue')

from phue import Bridge
import random
import time

b = Bridge() # Enter bridge IP here.

#If running for the first time, press button on bridge and run with b.connect() uncommented
#b.connect()

lights = b.get_light_objects()

sentence = input("Light command:") ##absolutely need this for a user-interactive program

if sentence == "Blink": 
        for light in lights:
                light.brightness = 254
                light.xy = [random.random(),random.random()]

##        timebeginning = time.time()

        while True:
                for light in lights:
                        light.brightness = 254
                        light.xy = [random.random(),random.random()]
##                        time.sleep(1) #makes it blink only once a second
##                duration = time.time()-timebeginning
##                if duration > 30:        ##makes it change colors for designated amount of time
##                        break

if sentence == "Red":
        for light in lights:
                light.brightness = 75
                light.xy = [0.675,0.322]

if sentence == "Orange":
        for light in lights:
                light.brightness = 75
                light.xy = [0.575,0.395]

if sentence == "Yellow":
        for light in lights:
                light.brightness = 75
                light.xy = [0.5,0.43]

if sentence == "Green":
        for light in lights:
                light.brightness = 75
                light.xy = [0.1,0.7] 

if sentence == "Blue":
        for light in lights:
                light.brightness = 75
                light.xy = [0.1,0.2]

if sentence == "Indigo":
        for light in lights:
                light.brightness = 75
                light.xy = [0.25,0.02] 

if sentence == "Violet":
        for light in lights:
                light.brightness = 75
                light.xy = [0.32,0.1]

if sentence == "Rainbow":
        for light in lights:
                light.brightness = 127
                light.xy = [(0.675,0.322),(0.575,0.395),(0.5,0.43), (0.1,0.7),(0.1,0.2),(0.25,0.02),(0.32,0.1)]  

        while True:
                for light in lights:
                        light.brightness = 127
                        light.xy = [random.random(),random.random()]
                        time.sleep(1) #this should make it wait 5 seconds in between shades
                        
                


