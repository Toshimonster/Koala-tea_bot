VERBOSE = True

import os
import sys
import requests
import random
import xlsxwriter
import io

from CONFIG import settings
from imgurpython import ImgurClient
from cmds import commands
from db import db
from teas import teatypes, peronitypes

import threading
import slackclient
import time
import datetime

PREFIX = settings["PREFIX"]
TEATIME_LENGTH_OG = settings["TEATIME_LENGTH"]
TEATIME_LENGTH = settings["TEATIME_LENGTH"]
client_id = settings["IMGUR_BOT_ID"]
client_secret = settings["IMGUR_BOT_SECRET"]
TENOR_KEY = settings["TENOR_KEY"]
BOT_TOKEN = settings["SLACK_BOT_TOKEN"]

thread = None
FLAG_TEATIME = False
TEATIME_TEAS = []
TEATIME_CREATOR = ''
TEATIME_CHANNEL = ''
TEATIME_END = 0
TEATIME_CANCELED = False

P_thread = None
P_FLAG_TEATIME = False
P_TEATIME_TEAS = []
P_TEATIME_CREATOR = ''
P_TEATIME_CHANNEL = ''
P_TEATIME_END = 0
P_TEATIME_CANCELED = False
P_TEATIME_LENGTH = TEATIME_LENGTH_OG

database = db("./db.json")
imgur = ImgurClient(client_id, client_secret)
koalatea = slackclient.SlackClient(BOT_TOKEN)

teatype_list = []
peroni_list = []

for teatype in teatypes:
    teatype_list.append(teatype[0])

for teatype in peronitypes:
    peroni_list.append(teatype[0])
#server stuff START

class server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print("Server Start")
        os.system("python -m http.server 8080")

serverthread = server()
serverthread.start()
#server stuff END

class ping_slackRequest_peroni(threading.Thread):
    def __init__(self, msg):
        threading.Thread.__init__(self)
        self.msg = msg

    def run(self):
        global P_TEATIME_CANCELED
        verbose("Thread Waiting")
        time.sleep((P_TEATIME_LENGTH) / 4)
        if not P_TEATIME_CANCELED:
            sendMessage(self.msg["channel"], '<!channel> Peroni is 1/4 done!')
        time.sleep((P_TEATIME_LENGTH) / 4)
        if not P_TEATIME_CANCELED:
            sendMessage(self.msg["channel"], '<!channel> Peroni is 1/2 done!')
        time.sleep((P_TEATIME_LENGTH) / 4)
        if not P_TEATIME_CANCELED:
            sendMessage(self.msg["channel"], '<!channel> Peroni is 3/4 done!')
        time.sleep((P_TEATIME_LENGTH) / 4)
        if not P_TEATIME_CANCELED:
            verbose("Thread Pinging")
            for i in range(5):
                koalatea.api_call("reactions.add", channel=self.msg["channel"], timestamp=self.msg["ts"], name="ballot_box_with_check")

class ping_slackRequest(threading.Thread):
    def __init__(self, msg):
        threading.Thread.__init__(self)
        self.msg = msg

    def run(self):
        global TEATIME_CANCELED
        verbose("Thread Waiting")
        time.sleep((TEATIME_LENGTH) / 4)
        if not TEATIME_CANCELED:
            sendMessage(self.msg["channel"], '<!channel> Teatime is 1/4 done!')
        time.sleep((TEATIME_LENGTH) / 4)
        if not TEATIME_CANCELED:
            sendMessage(self.msg["channel"], '<!channel> Teatime is 1/2 done!')
        time.sleep((TEATIME_LENGTH) / 4)
        if not TEATIME_CANCELED:
            sendMessage(self.msg["channel"], '<!channel> Teatime is 3/4 done!')
        time.sleep((TEATIME_LENGTH) / 4)
        if not TEATIME_CANCELED:
            verbose("Thread Pinging")
            for i in range(5):
                koalatea.api_call("reactions.add", channel=self.msg["channel"], timestamp=self.msg["ts"], name="ballot_box_with_check")

def createXcel():
    workbook = xlsxwriter.Workbook('Data.xlsx')
    title = workbook.add_format({"bold": True, "align": "center", "font_size": 14})
    norm  = workbook.add_format({"italic": True, "align": "center"})
    worksheet = workbook.add_worksheet()
    worksheet.set_column('B:B', 15)
    worksheet.set_column('C:C', 15)
    worksheet.set_column('D:D', 15)
    worksheet.set_column('E:E', 15)
    worksheet.write(1, 1, "User", title)
    worksheet.write(1, 2, "Drinks Made", title)
    worksheet.write(1, 3, "Drinks Drunk", title)
    worksheet.write(1, 4, "Ratio", title)
    sorteddb = sorted(database.data.items(), key=lambda x: tryDivide('(x[1]["drinks"]/x[1]["made"])', x))
    for index, user in enumerate(sorteddb):
        worksheet.write(index + 2, 0 , index + 1, norm)
        worksheet.write(index + 2, 1 , userInfo(user[0])['name'], norm)
        worksheet.write(index + 2, 2 , user[1]["made"], norm)
        worksheet.write(index + 2, 3 , user[1]["drinks"], norm)
        worksheet.write(index + 2, 4 , str(tryDivide('(x[1]["made"]/x[1]["drinks"])', user)), norm)
    worksheet.insert_image('F3', 'KoalaTea.jpg')
    workbook.close()

def getId(username):
    id = False
    api_call = koalatea.api_call("users.list")
    if api_call.get("ok"):
        users = api_call.get("members")
        for user in users:
            if 'name' in user and user.get('name') == username:
                id = user.get('id')
    return id

def isAnimated(obj):
    return obj.animated

def tryDivide(exp, x):
    x = x
    try:
        return eval(exp)
    except ZeroDivisionError:
        return float('inf')

def checkTea(value):
    for drink in teatypes:
        if value.title() == drink[0] or value.lower() in drink[1]:
            return drink[0]
    if value.lower().split(" ")[0] == 'custom':
        return " ".join(value.split(" ")[1:])
    return False

def P_checkTea(value):
    for drink in peronitypes:
        if value.title() == drink[0] or value.lower() in drink[1]:
            return drink[0]
    if value.lower().split(" ")[0] == 'custom':
        return " ".join(value.split(" ")[1:])
    return False

def verbose(msg):
    if VERBOSE:
        print(msg)

def mention(user):
    return "<@"+user+">"

def addReaction(msg, reaction):
    koalatea.api_call("reactions.add", channel=msg["channel"], timestamp=msg["ts"], name=reaction)

def sendMessage(channel, text):
    koalatea.api_call("chat.postMessage", channel=channel, text=text, as_user=True)

def upload_file(filename, content, channel):
        ret = koalatea.api_call("files.upload", filename=filename, channels=channel, file= io.BytesIO(content))
        if not 'ok' in ret or not ret['ok']:
            verbose('fileUpload failed ' + ret['error'])
            return False
        else:
            return True

def userInfo(user):
    call = koalatea.api_call("users.info", user=user)
    if call["ok"]:
        return call["user"]
    else:
        raise("ERROR WITH users.info")

def parse_to_event(slack_rtm_output):
    global FLAG_TEATIME
    global TEATIME_CREATOR
    global TEATIME_CHANNEL
    global TEATIME_END
    global TEATIME_CANCELED
    global P_FLAG_TEATIME
    global P_TEATIME_CREATOR
    global P_TEATIME_CHANNEL
    global P_TEATIME_END
    global P_TEATIME_CANCELED
    if FLAG_TEATIME:
        if len(slack_rtm_output) > 0:

            verbose("TEATIME! : " + str(TEATIME_END - time.time()))
            if TEATIME_END < time.time():
                FLAG_TEATIME = False
                teatimeEnd()

            eventType = slack_rtm_output[0]["type"]

            if eventType == "message":
                if TEATIME_CHANNEL == slack_rtm_output[0]["channel"]:
                    if slack_rtm_output[0]["text"][len(PREFIX):].split(" ")[0].lower() == 'cancel':
                        sendMessage(TEATIME_CHANNEL, '<@channel> ' + mention(slack_rtm_output[0]["user"]) + ' has canceled the tearound! No more koala-tea drinks. :(')
                        FLAG_TEATIME = False
                        TEATIME_CANCELED = True
                    elif slack_rtm_output[0]["text"].lower() == 'cancel':
                        for tindex, tdrink in enumerate(TEATIME_TEAS):
                            if tdrink[0] == slack_rtm_output[0]["user"]:
                                TEATIME_TEAS.pop(tindex)
                        addReaction(slack_rtm_output[0], "x")

                    try:
                        teatype = checkTea(slack_rtm_output[0]["text"])

                        if teatype != False:
                            TEATIME_TEAS.append([teatype, slack_rtm_output[0]["user"]])
                            addReaction(slack_rtm_output[0], "ballot_box_with_check")
                    except Exception as e:
                        verbose("EXCEPTION :")
                        verbose(e)

                if not TEATIME_CANCELED:
                    try:
                        user = slack_rtm_output[0]["user"]
                        channel = text = slack_rtm_output[0]["channel"]
                        text = slack_rtm_output[0]["text"]
                        event_onMessage(text, user, channel, slack_rtm_output[0])
                    except Exception as e:
                        verbose("EXCEPTION :")
                        verbose(e)
    elif P_FLAG_TEATIME:
        if len(slack_rtm_output) > 0:

            verbose("PERONI! : " + str(P_TEATIME_END - time.time()))
            if P_TEATIME_END < time.time():
                P_FLAG_TEATIME = False
                P_teatimeEnd()

            eventType = slack_rtm_output[0]["type"]

            if eventType == "message":
                if P_TEATIME_CHANNEL == slack_rtm_output[0]["channel"]:
                    if slack_rtm_output[0]["text"][len(PREFIX):].split(" ")[0].lower() == 'cancel':
                        sendMessage(P_TEATIME_CHANNEL, '<@channel> ' + mention(slack_rtm_output[0]["user"]) + ' has canceled the peroni! No more countdown hums. :(')
                        P_FLAG_TEATIME = False
                        P_TEATIME_CANCELED = True
                    elif slack_rtm_output[0]["text"].lower() == 'cancel':
                        for tindex, tdrink in enumerate(P_TEATIME_TEAS):
                            if tdrink[0] == slack_rtm_output[0]["user"]:
                                P_TEATIME_TEAS.pop(tindex)
                        addReaction(slack_rtm_output[0], "x")

                    try:
                        teatype = P_checkTea(slack_rtm_output[0]["text"])

                        if teatype != False:
                            P_TEATIME_TEAS.append([teatype, slack_rtm_output[0]["user"]])
                            addReaction(slack_rtm_output[0], "ballot_box_with_check")
                    except Exception as e:
                        verbose("EXCEPTION :")
                        verbose(e)

                if not TEATIME_CANCELED:
                    try:
                        user = slack_rtm_output[0]["user"]
                        channel = text = slack_rtm_output[0]["channel"]
                        text = slack_rtm_output[0]["text"]
                        event_onMessage(text, user, channel, slack_rtm_output[0])
                    except Exception as e:
                        verbose("EXCEPTION :")
                        verbose(e)

    else:
        if len(slack_rtm_output) > 0:
            eventType = slack_rtm_output[0]["type"]

            if eventType == "message":
                try:
                    user = slack_rtm_output[0]["user"]
                    channel = text = slack_rtm_output[0]["channel"]
                    text = slack_rtm_output[0]["text"]
                    event_onMessage(text, user, channel, slack_rtm_output[0])
                except Exception as e:
                    verbose("EXCEPTION :")
                    verbose(e)

def event_onMessage(message, user, channel, p_msg):
    if message.startswith(PREFIX):
        flag_found = False
        command = message[len(PREFIX):].split(" ")[0].lower()
        arguments = message.split(" ")[1:]
        for cmd in commands:
            if command in cmd["alias"]:
                flag_found = True
                exec(cmd["execute"])
        if not flag_found:
            sendMessage(channel, mention(user) + " : '" + command + "' is not a real command!")

def teatimeEnd():
    global TEATIME_CREATOR
    global TEATIME_CHANNEL
    global TEATIME_TEAS

    sendMessage(TEATIME_CHANNEL, "Teatime done! Generating Koala-tea drink lists...")

    try:
        database.data[TEATIME_CREATOR]["made"] += len(TEATIME_TEAS)
    except:
        database.data[TEATIME_CREATOR] = {
            "drinks" : 0,
            "made" : len(TEATIME_TEAS)
        }
    drinks = ''
    for tdrink in TEATIME_TEAS:
        try:
            database.data[tdrink[1]]["drinks"] += 1
        except:
            database.data[tdrink[1]] = {
                "drinks" : 1,
                "made" : 0
            }

    for teatype in teatypes:
        this_tea_value = 0
        this_tea_text = ''
        for tdrink in TEATIME_TEAS:
            if tdrink[0] == teatype[0]:
                this_tea_text += "_" + userInfo(tdrink[1])["name"] + "_\n"
                this_tea_value += 1
        if this_tea_value > 0:
            this_tea_text = "*" + teatype[0] + " - " + str(this_tea_value) + "*\n" + this_tea_text
        drinks += this_tea_text

    custom_tea_value = 0
    custom_tea_text = ''
    for tdrink in TEATIME_TEAS:
        if tdrink[0] not in teatype_list:
            custom_tea_text += "_" + userInfo(tdrink[1])["name"] + " wants a " + tdrink[0] + "_\n"
            custom_tea_value += 1
    if custom_tea_value > 0:
        custom_tea_text = "*Custom Drinks - " + str(custom_tea_value) + "*\n" + custom_tea_text
    drinks += custom_tea_text

    database.write()
    sendMessage(TEATIME_CHANNEL, mention(TEATIME_CREATOR) + " Drinks are recorded!\n\n" + drinks + "\n *I hope you enjoy your Koala-tea drinks!*")

def P_teatimeEnd():
    global P_TEATIME_CREATOR
    global P_TEATIME_CHANNEL
    global P_TEATIME_TEAS

    sendMessage(P_TEATIME_CHANNEL, "Peroni done! Generating Koala-tea drink lists...")

    drinks = ''

    for teatype in peronitypes:
        this_tea_value = 0
        this_tea_text = ''
        for tdrink in P_TEATIME_TEAS:
            if tdrink[0] == teatype[0]:
                this_tea_text += "_" + userInfo(tdrink[1])["name"] + "_\n"
                this_tea_value += 1
        if this_tea_value > 0:
            this_tea_text = "*" + teatype[0] + " - " + str(this_tea_value) + "*\n" + this_tea_text
        drinks += this_tea_text

    custom_tea_value = 0
    custom_tea_text = ''
    for tdrink in P_TEATIME_TEAS:
        if tdrink[0] not in peroni_list:
            custom_tea_text += "_" + userInfo(tdrink[1])["name"] + " wants a " + tdrink[0] + "_\n"
            custom_tea_value += 1
    if custom_tea_value > 0:
        custom_tea_text = "*Custom Drinks - " + str(custom_tea_value) + "*\n" + custom_tea_text
    drinks += custom_tea_text

    sendMessage(P_TEATIME_CHANNEL, mention(P_TEATIME_CREATOR) + " Drinks are recorded!\n\n" + drinks + "\n *I hope you enjoy your Koala-tea drinks!*")


if __name__ == "__main__":
    connection = koalatea.rtm_connect()
    if connection:
        print("KoalaTea is up and running!")
        while True:
            try:
                parse_to_event(koalatea.rtm_read())
            except Exception as e:
                verbose('MAJOR ERROR :')
                verbose(e)
            time.sleep(0.25)

    else:
        print("Connection Failed!")
        print(connection)
