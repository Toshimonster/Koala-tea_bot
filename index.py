VERBOSE = True

from cmds import commands
from db import db
from teas import teatypes

import slackclient
import time

FLAG_TEATIME = False
TEATIME_TEAS = []
TEATIME_CREATOR = ''
TEATIME_CHANNEL = ''
BOT_TOKEN = 'xoxb-203556679653-cw7sHS1qdXwTQsfd5Gs0BGoj'
PREFIX = '!'
TEATIME_END = 0

database = db("./db.json")
koalatea = slackclient.SlackClient(BOT_TOKEN)

def verbose(msg):
    if VERBOSE:
        print(msg)

def mention(user):
    return "<@"+user+">"

def sendMessage(channel, text):
    koalatea.api_call("chat.postMessage", channel=channel, text=text, as_user=True)

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
    if FLAG_TEATIME:
        if len(slack_rtm_output) > 0:

            print("TEATIME!", TEATIME_END - time.time())
            if TEATIME_END < time.time():
                FLAG_TEATIME = False
                teatimeEnd()
                
            eventType = slack_rtm_output[0]["type"]

            if eventType == "message":
                if TEATIME_CHANNEL == slack_rtm_output[0]["channel"]:
                    teatype = slack_rtm_output[0]["text"]
                    
                    if teatype.lower() in teatypes:
                        TEATIME_TEAS.append([teatype, slack_rtm_output[0]["user"]])
    else:
        if len(slack_rtm_output) > 0:
            eventType = slack_rtm_output[0]["type"]

            if eventType == "message":
                try:
                    user = slack_rtm_output[0]["user"]
                    channel = text = slack_rtm_output[0]["channel"]
                    text = slack_rtm_output[0]["text"]
                    event_onMessage(text, user, channel)
                except:
                    verbose("Couldent get attributes of a message event.")

def event_onMessage(message, user, channel):
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

    verbose(TEATIME_TEAS)

    sendMessage(TEATIME_CHANNEL, "Teatime done! Generating Koala-tea drink lists...")
    
    try:
        database.data[TEATIME_CREATOR]["rounds"] += 1
    except:
        database.data[TEATIME_CREATOR] = {
            "teas" : 0,
            "rounds" : 1
        }
    drinks = ''
    for tdrink in TEATIME_TEAS:
        try:
            database.data[tdrink[1]]["teas"] += 1
        except:
            database.data[tdrink[1]] = {
                "teas" : 1,
                "rounds" : 0
            }
        drinks += userInfo(tdrink[1])["name"] + " wants a " + tdrink[0] + "\n"
    database.write()
    sendMessage(TEATIME_CHANNEL, mention(TEATIME_CREATOR) + " Drinks are recorded!\n\n" + drinks + "\n *I hope you enjoy your Koala-tea drinks!*")

if __name__ == "__main__":
    if koalatea.rtm_connect():
        print("KoalaTea is up and running!")
        while True:
            parse_to_event(koalatea.rtm_read())
            time.sleep(1)
        
    else:
        print("Connection Failed!")

