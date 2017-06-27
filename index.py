VERBOSE = True

import os
import sys
import requests
import random

from imgurpython import ImgurClient
from cmds import commands
from db import db
from teas import teatypes

import threading
import slackclient
import time

client_id = '090b7b857de4107'
client_secret = '0df30a05bdfb38985ac85e7a15c56e6087308ccf'

FLAG_TEATIME = False
TEATIME_TEAS = []
TEATIME_CREATOR = ''
TEATIME_CHANNEL = ''
BOT_TOKEN = 'xoxb-203556679653-cw7sHS1qdXwTQsfd5Gs0BGoj'
PREFIX = '!'
TEATIME_END = 0

database = db("./db.json")
imgur = ImgurClient(client_id, client_secret)
koalatea = slackclient.SlackClient(BOT_TOKEN)

class ping_slackRequest(threading.Thread):
    def __init__(self, msg):
        threading.Thread.__init__(self)
        self.msg = msg
    
    def run(self):
        verbose("Thread Waiting")
        time.sleep(60)
        verbose("Thread Pinging")
        for i in range(5):
            koalatea.api_call("reactions.add", channel=self.msg["channel"], timestamp=self.msg["ts"], name="ballot_box_with_check")
    

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
                    try:
                        teatype = checkTea(slack_rtm_output[0]["text"])
                    
                        if teatype != False:
                            TEATIME_TEAS.append([teatype, slack_rtm_output[0]["user"]])
                            addReaction(slack_rtm_output[0], "ballot_box_with_check")
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
        drinks += userInfo(tdrink[1])["name"] + " wants a " + tdrink[0] + "\n"
    database.write()
    sendMessage(TEATIME_CHANNEL, mention(TEATIME_CREATOR) + " Drinks are recorded!\n\n" + drinks + "\n *I hope you enjoy your Koala-tea drinks!*")

if __name__ == "__main__":
    if koalatea.rtm_connect():
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

