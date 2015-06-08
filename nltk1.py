import nltk
import sys
sys.path.append('/Users/lydiamonirian/Desktop/phue')

from phue import Bridge

b = Bridge()

lights = b.get_light_objects()

sentence = input("What would you like?") ##computer asks
tokens = nltk.word_tokenize(sentence) ##inspects each word

#for word in tokens:
#    if (word.startswith('happ')):
#        print("This sentence has happy in it!")

#tokens
tagged = nltk.pos_tag(tokens) ##assigns each word part of speech
#print "Is this JJ? %s" % (tagged[4][1])
#print ("Tagged is %s") % (tagged)

for tuple in tagged:
        if (tuple[1] == "JJ"): ##honing in on adjective
            #print("I found JJ!")
            if (tuple[0].startswith("happ")):
                print "Be happy!"
                for light in lights:
                    light.brightness = 254
                    light.xy = [0.5, 0.44] #Yellow
            #elif (tuple[0].startswith("sad")):
                #print ("Don't be sad!")
                #for light in lights:
                    #light.brightness = 254
                    #light.xy = [0.1, 0.15] #Blue
            elif (tuple[0].startswith("angry")):
                print ("Try to calm down.")
                for light in lights:
                    light.brightness = 254
                    light.xy = [0.15, 0.7] #Green
            elif (tuple[0].startswith("nerv")):
                print ("Try to calm down.")
                for light in lights:
                    light.brightness = 254
                    light.xy = [0.15, 0.7] ##all of these have to be JJ in "i want to be..." or "I am..." form
            ##elif (tuple[0].startswith("dark")):
                
                       
for tuple in tagged:
    if (tuple[1] == "NN"): ##honing in on noun
         if (tuple[0].startswith("awake")):
             print "Blue lighting prohibits melatonin production."
             for light in lights:
                 light.brightness = 254
                 light.xy = [0.1, 0.15] ##for phrases like "I need to stay..."

                     

#tagged[0:5]
#if tagged[4][1] == 'happy':

#print "Sentence is: %s " % sentence

#if sentence == "I want to be happy":
#    for w in sentence:
#        print w
    #if [w for w in sentence if w.startsswith('happ')]:
    #    print "We're executing code!"
        #for light in lights:
#            light.brightness = 254
#            light.xy = [(0.5, 0.44)]

print "End of our program!"
        
