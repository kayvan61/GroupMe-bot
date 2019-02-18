import duel
from pprint import pprint as pprint
from os import listdir
from os.path import isfile, join
from random import randrange, choice
import importlib
from PIL import Image
import csv
import re
from coolFaces import face
import asyncio
import json
import http.client
import urllib
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import mmap

_STATS_ = []
_VERSION_ = '0.0.1'
_BOTID_ = ''
inJson = None

onlyfiles = [f for f in listdir("./memes") if isfile(join("./memes", f))]
onlyJojos = [f for f in listdir("./jojos") if isfile(join("./jojos", f))]
curDuel = None
modules = []

regexes = [
    re.compile('^\/coolGuy', re.IGNORECASE),
    re.compile('^\/version', re.IGNORECASE),
    re.compile('^\/shrug', re.IGNORECASE),
    re.compile('roasted', re.IGNORECASE),
    re.compile('^\/help', re.IGNORECASE),
    re.compile('^\/lewd', re.IGNORECASE),
    re.compile('^\/seals', re.IGNORECASE),
    re.compile('^\/stats', re.IGNORECASE),
    re.compile('normie', re.IGNORECASE),
    re.compile('^\/nuke', re.IGNORECASE),
    re.compile('^\/custNuke', re.IGNORECASE),
    re.compile('^\/memePlz', re.IGNORECASE),
    re.compile('^\/startDuel', re.IGNORECASE),
    re.compile('^\/joinDuel', re.IGNORECASE),
    re.compile('^\/getDuelStat', re.IGNORECASE),
    re.compile('^\/jojosPlz', re.IGNORECASE),
    re.compile('^\/Hayato', re.IGNORECASE),
    re.compile('^\/rgbNuke', re.IGNORECASE)
]

options = {}

inStr = ''


def postMessage(a, BOTID=_BOTID_):
    body = {
        "bot_id": BOTID,
        "text": a
    }  # Set POST fields here

    url = 'https://api.groupme.com/v3/bots/post'

    print(a + " to " + BOTID)

    print(url)

    try:
        req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'),
                                     headers={'content-type': 'application/json'})
        response = urllib.request.urlopen(req)
        if response.status > 204:
            raise()
        print(response.status)
    except Exception as ex:
        print('something fucked up yo: ' + str(ex))


def postPicture(path, BOTID=_BOTID_):

    post_url = 'https://api.groupme.com/v3/bots/post'

    url = 'https://image.groupme.com/pictures'

    with open(path, "rb") as imageFile:
        f = imageFile.read()
        imgData = bytearray(f)

    try:
        #upload image
        req = urllib.request.Request(url, data = imgData,
                                     headers = {'content-type': 'image/jpeg',
                                                'X-Access-Token': ''})
        response = urllib.request.urlopen(req)
        if response.status > 204:
            raise()
        inData = json.loads(response.read().decode('utf-8'))
        imgURL = inData['payload']['picture_url']
        
        #create the post with now uploaded image
        body = {
            "attachments": [{'type': 'image',
                             'url': imgURL}],
            "bot_id": BOTID
        }  # Set POST fields here
        pprint(json.dumps(body))
        req = urllib.request.Request(post_url, data=json.dumps(body).encode('utf-8'),
                                     headers={'content-type': 'application/json'})
        response = urllib.request.urlopen(req)
        if response.status > 204:
            raise()
        print(response.status)
    except Exception as ex:
        print("couldn't upload image: " + str(ex))


def startDuel():
    global curDuel
    postMessage("starting duel, type /joinDuel to join")
    try:
        strings = inStr[inStr.index(' '):]
    except ValueError:
        strings = ""
    strings = strings.strip()
    if strings != "":
        print("time spec")
        d = duel.duel(int(strings), inJson['name'])
    else:
        print("no time spec")
        d = duel.duel(500, inJson['name'])
    thread = d.startDuel()
    curDuel = d

    updateStats("startDuel")


def joinDuel():
    global curDuel
    if curDuel == None or curDuel.isDone():
        postMessage("sorry. no on going duel")
    else:
        curDuel.addPlayer(inJson['name'])
        postMessage("player "+ inJson['name'] + " joined!")


def getDuelStat():
    global curDuel
    if curDuel == None or curDuel.isDone():
        postMessage("sorry. no on going duel")
    else:
        curDuel.getLobbyState()
    updateStats("getDuelStat")

def writeToFile():
    global _STATS_
    with open('stats.meme', 'w+', newline='') as csvfile:
        print('file open')
        writer = csv.writer(csvfile, delimiter=",", quotechar='|')
        print('writing')
        writer.writerows(_STATS_)
        csvfile.flush()


def updateStats(s):
    index = -1
    print(len(_STATS_))
    for item in _STATS_:
        # print('in for loop')
        if item[0] == s:
            index = item
    if index != -1:
        index = _STATS_.index(index)
        _STATS_[index] = (_STATS_[index][0], str(int(_STATS_[index][1]) + 1))

        writeToFile()


def nuke():
    #print(bot.inJson)
    #print('from nuke')

    try:
        pictureUrl = inJson['attachments'][0]['url']
        request.urlretrieve(pictureUrl, "temp_nuke.jpg")
    except Exception as ex:
        print('from nuke')
        print(str(ex))

    try:
        image = Image.open('temp_nuke.jpg')
        image.point(lambda i: i*113 % 1320 % 255).save('temp_nuke.jpg')
    except Exception as ex:
        print('from nuke')
        print(str(ex))

    try:
        postPicture('temp_nuke.jpg')
    except Exception as ex:
        print('from nuke')
        print(str(ex))

    updateStats('nuke')


def memePlz():
#    postMessage("duckkkkkk")
    postPicture(join("./memes", onlyfiles[randrange(0, len(onlyfiles)-1 )] ))
    updateStats('memePlz')


def jojosPlz():
    postPicture(join("./jojos", choice(onlyJojos)))
    updateStats('jojosPlz')


def custNuke():

    strings = inStr[inStr.index(' '):]

    try:
        pictureUrl = inJson['attachments'][0]['url']
        request.urlretrieve(pictureUrl, "temp_nuke.jpg")
    except Exception as ex:
        print('from nuke')
        print(str(ex))

    try:
        image = Image.open('temp_nuke.jpg')
        exec("""image.point(lambda i: """ + strings+ """).save('temp_nuke.jpg')""")
    except Exception as ex:
        print('from nuke')
        print(str(ex))

    try:
        postPicture('temp_nuke.jpg')
    except Exception as ex:
        print('from nuke')
        print(str(ex))

    updateStats('custNuke')


def lewd():
    postMessage('DONT LEWD THE LOLI BOT!', _BOTID_)

    updateStats('lewd')


def normie():
    postMessage('REEEEEEEEEEEEEEEEEEEEEE', _BOTID_),  # normie

    updateStats('normie')


def shrug():
    postMessage('¯\_(ツ)_/¯', _BOTID_),  # /shrug

    updateStats('shrug')


def roasted():
    postMessage('RIASTED*', _BOTID_),  # roasted

    updateStats('roasted')


def version():
    versionStr = 'Version: ' + _VERSION_ + ' Pyth\n \
                Author: Ali Macaroni\n \
                Lang: Python3\n \
                PLZ NO BAMBOOZLE'
    postMessage(versionStr, _BOTID_)

    updateStats('version')


def find_nth_over(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+1)
        n -= 1
    return start


def rgbNuke():
    strings = inStr[inStr.index(' '):]
    r_str = strings[strings.index('(')+1:find_nth_over(strings, ',', 1)]
    g_str = strings[find_nth_over(strings, ',', 1)+1: find_nth_over(strings, ',', 2)]
    b_str = strings[find_nth_over(strings, ',', 2)+1: find_nth_over(strings, ')', 1)]

    print(r_str)
    print(g_str)
    print(b_str)
    r_c = None
    g_c = None
    b_c = None

    try:
        pictureUrl = inJson['attachments'][0]['url']
        request.urlretrieve(pictureUrl, "temp_nuke.jpg")
    except Exception as ex:
        pass

    try:
        image = Image.open('temp_nuke.jpg')
        image.load()
        r_c = eval("""image.split()[0].point(lambda i: """ + r_str + """)""", globals(), locals())
        g_c = eval("""image.split()[1].point(lambda i: """ + g_str + """)""", globals(), locals())
        b_c = eval("""image.split()[2].point(lambda i: """ + b_str + """)""", globals(), locals())
        print(r_c, '\n', g_c, '\n', b_c)
    except Exception as ex:
        print('from rgb nuke lambdas')
        print(str(ex))

    try:
        im = Image.merge("RGB",(r_c,g_c,b_c))
        im.save("temp_nuke.jpg")
    except Exception as ex:
        print("from rgb nuke merge")
        print(str(ex))
        print("-----------------")


    try:
        postPicture('temp_nuke.jpg')
    except Exception as ex:
        print('from rgb nuke post')
        print(str(ex))

    updateStats('custNuke')



def seals():
    postMessage(
        r"""What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals, and I've been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I'm the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You're fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that's just with my bare hands.""",
        _BOTID_)
    postMessage(
        r"""Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little "clever" comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn't, you didn't, and now you're paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You're fucking dead, kiddo.""",
        _BOTID_)

    updateStats('seals')


def stats():
    statStr = ''
    temp = ''
    updateStats('/stats')
    with open('stats.meme', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            temp = str(row)
            statStr += (temp[1:len(temp) - 1] + '\n').replace("'", "")
    postMessage(statStr, _BOTID_)


def coolGuy():
    postMessage(face(), _BOTID_)

    updateStats('coolGuy')


def help():
    helpStr = ''
    for func in options:
        print(type(func))
        print(func)
        helpStr += '/' + options[func].__name__ + '\n'
    postMessage(helpStr, _BOTID_)

    updateStats('help')


def Hayato():
    postPicture("./Hayato.jpg")
    
    updateStats('hayato')


def checkReg(incomingString, jsonRaw):
    index = -1

    global inStr, inJson
    inStr = incomingString
    inJson = json.loads(jsonRaw[jsonRaw.index('{'):])
    #print(inJson)

    try:
        pprint(inJson) #used to get all the fields
        pictureUrl = inJson['attachments'][0]['url']
        urllib.request.urlretrieve(pictureUrl, "temp_nuke.jpg")
    except Exception as ex:
        pass

    for i in range(0, len(regexes)):
        if regexes[i].search(incomingString):
            index = i
            break

    try:
        options[index]()
    except ValueError as ex :
        print('dont care: '+str(ex))
    except KeyError as ex:
        print('dont care')


def init(restart = False):
    global _STATS_, options
    options = {0: coolGuy,  # /cool guy
               1: version,  # /version
               2: shrug,  # /shrug
               3: roasted,  # roasted
               4: help,  # /help
               5: lewd,  # /lewd
               6: seals,  # /seals
               7: stats,  # /stats
               8: normie,  # normie
               9: nuke,
               10: custNuke,
               11: memePlz,
               12: startDuel,
               13: joinDuel,
               14: getDuelStat,
               15: jojosPlz,
               16: Hayato,
               17: rgbNuke
}
    with open('stats.meme', newline='') as file:
        r = csv.reader(file)
        temp = [l for l in r]
        _STATS_ = [tuple(l) for l in temp]
    if not restart:
        print("awake")
    with open('test.meme', 'r+') as file:
        file.seek(0)
        for cmd in file:
            if cmd == '' or cmd == '\n' :
                continue
            print(cmd)
            #add(cmd,True)



