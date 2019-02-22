import pymongo
from pymongo import MongoClient
import json
import requests
import random
import string
from pprint import pprint

#################################################
#Get greetings
with open('Greetings', 'r') as f:
    lg = f.read()
lg = lg.split("\n")
#End getting greetings
#################################################
#Get farewells
with open('Farewells', 'r') as f:
    lf = f.read()
lf = lf.split("\n")
#End getting Farewells
#################################################
#List of Cities
with open('city.list.json', encoding='utf-8') as f:
    listOfCities = json.loads(f.read())
lcn = []
for i in range(len(listOfCities)) :
    if(listOfCities[i]['name'] != "") :
        lcn.append(listOfCities[i]['name'])
#finish making list of city names
#################################################

print("Hello there! What's your name? ")
response = input("")
name = response
if(response.lower() != "bye") :
    x = random.randint(0,15)
    print(lg[x].capitalize() + " " + name + "!")

while('bye' not in response.lower()) :

    rl = response.lower()

    print("Would you like to use the dictionary or find the weather?");
    rl = input("").lower()

    #Begin Weather
    if('weather' in rl or 'climate' in rl or 'temperature' in rl) :
        city = input("What city would you like to find the weather for? ")
        valid = False
        for i in range(len(lcn)) :
            if city.lower() == lcn[i].lower() :
                city = lcn[i]
                print("found: " + lcn[i] + " : "+ str(len(lcn[i])))
                valid = True
            elif (i == len(lcn) -1 and valid == False) :
                print("Error: Please enter valid city")

        if valid == True :
            #This weather forecast uses the openweathermap api. This program requires you to put your own personal appid.
            url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=Imperial&appid=--------------------------------'
            data = requests.get(url)
            dj = json.loads(data.text)
                #print(type(data.text))
                #print(data.text)
            print('\n')
            #print(data.text)
            print('\n')
            if dj['weather'][0]['main'] == 'Clouds' :
                f = open('CloudsArt', 'r')
                print(f.read())
                print("The weather is cloudy")
            elif dj['weather'][0]['main'] == 'Thunderstorm' :
                f = open('ThunderstormArt', 'r')
                print(f.read())
                print("There is a thunderstorm. Don't forget your umbrella!")
            elif dj['weather'][0]['main'] == 'Rain' :
                f = open('RainArt', 'r')
                print(f.read())
                print("The weather is rainy. Don't forget your umbrella!")
            elif dj['weather'][0]['main'] == 'Drizzle' :
                f = open('DrizzleArt', 'r')
                print(f.read())
                print("There is a drizzle. Don't forget your umbrella!")
            elif dj['weather'][0]['main'] == 'Snow' :
                f = open('SnowArt', 'r')
                print(f.read())
                print("There is snow! Don't slip!")
            elif dj['weather'][0]['main'] == 'Clear' :
                f = open('ClearArt', 'r')
                print(f.read())
                print("Clear skies!")
            else:
                f = open('AtmosphereArt', 'r')
                print(f.read())
                print("It's hard to see...")

            print("The current temperature is " + str(dj['main']['temp']) + " F")
            print("The temperature will reach a high of " + str(dj['main']['temp_max']) + " F")
            print("The temperature will reach a low of " + str(dj['main']['temp_min']) + " F")
    #End Weather
    #################################################
    #Start Dictionary (Oxford Dictionary)
    elif('dictionary' in rl or 'dict' in rl) :
        #This dictionary uses the Oxford Dictionary API.
        app_id = '-------'
        app_key = '--------------------------------'
        language = "en";
        print("Definition, synonym, or translate?");
        choice = input("");

        if(choice.lower() in "definition") :
            language = 'en'
            word_id = input("Word: ")
            try :
                url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id.lower()
                r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

                data = r;
                dj = json.loads(data.text)
                #print("code {}\n".format(r.status_code))
                #print("text \n" + r.text)
                #print("json \n" + json.dumps(r.json()))

                print('\n')
                print(str(dj['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]))
                print('\n')
            except:
                print("Enter valid word next time.")
                print("\n")
        elif(choice.lower() in "synonym") :
            language = 'en'
            word_id = input("Word: ")
            try :
                url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id.lower() + '/synonyms;antonyms'
                r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
                data = r;
                dj = json.loads(data.text)
                #print("code {}\n".format(r.status_code))
                #print("text \n" + r.text)
                #print("json \n" + json.dumps(r.json()))
                print('\n')
                synonyms = dj['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['subsenses'][0]['synonyms']
                for s in range(len(synonyms)):
                    print(synonyms[s]['text'])
                print('\n')
            except:
                print("None")
                print("\n")
        elif (choice.lower() in "translate") :
            print("This is strictly an English to Spanish translator!")
            app_id = '6bbd5b79'
            app_key = 'b734024385206b0d7baa7659608c6419'

            source_language = 'en'
            target_language = 'es'
            word_id = input("Word: ")
            print("\n")
            try:
                valid = False
                url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + source_language + '/' + word_id.lower() + '/translations=' + target_language
                r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
                data = r;
                dj = json.loads(data.text)
                trans = dj['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['translations']
                finished = []
                for i in range(len(trans)):
                    next = trans[i]["text"]
                    ok = True
                    for j in finished:
                        if j in next:
                            ok = False
                    if ok == True :
                        print(trans[i]["text"])
                        finished.append(next)
                valid = True
            except:
                try:
                    if(valid == False):
                        try:
                            url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + source_language + '/' + word_id.lower() + '/translations=' + target_language

                            r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
                            data = r;
                            dj = json.loads(data.text)
                            trans = dj['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['subsenses'][0]['translations']
                            finished = []
                            for i in range(len(trans)):
                                next = trans[i]["text"]
                                ok = True
                                for j in finished:
                                    if j in next:
                                        ok = False
                                if ok == True :
                                    print(trans[i]["text"])
                                    finished.append(next)
                        except:
                            #Translate doesn't register plural words so this second half repeats the original translate code.
                            #The only difference is that the word loses the 's' at the of the word if it's plural
                            #If the word truly doesn't exist, then the code will print out "Invalid"
                            if(word_id.endswith('s') and valid == False) :
                                word_id = word_id[:-1]
                                try:
                                    valid = False
                                    url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + source_language + '/' + word_id.lower() + '/translations=' + target_language
                                    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
                                    data = r;
                                    dj = json.loads(data.text)
                                    trans = dj['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['translations']
                                    finished = []
                                    for i in range(len(trans)):
                                        next = trans[i]["text"]
                                        ok = True
                                        for j in finished:
                                            if j in next:
                                                ok = False
                                        if ok == True :
                                            print(trans[i]["text"])
                                            finished.append(next)
                                    valid = True
                                except:
                                    try:
                                        if(valid == False):
                                            try:
                                                url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + source_language + '/' + word_id.lower() + '/translations=' + target_language

                                                r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
                                                data = r;
                                                dj = json.loads(data.text)
                                                trans = dj['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['subsenses'][0]['translations']
                                                finished = []
                                                for i in range(len(trans)):
                                                    next = trans[i]["text"]
                                                    ok = True
                                                    for j in finished:
                                                        if j in next:
                                                            ok = False
                                                    if ok == True :
                                                        print(trans[i]["text"])
                                                        finished.append(next)
                                            except:
                                                print("Invalid")
                                    except:
                                        print("Invalid")
                            else:
                                print("Invalid")
                except:
                    print("Invalid")

        print("\n")
    elif "bye" in rl :
        if 'bye' in rl :
            x = random.randint(0,12)
            print(lf[x].capitalize() + " " + name + "!")
        break;
    else :
        print("Try again...")
    response = ""

#Exit Conversation
if 'bye' in response.lower() :
    if(name.lower() != 'bye') :
        x = random.randint(0,12)
        print(lf[x].capitalize() + " " + name + "!")
    else:
        x = random.randint(0,12)
        print(lf[x].capitalize()+"!")
