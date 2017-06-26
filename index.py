from cmds import commands

import slackclient
import time

BOT_TOKEN = 'xoxb-203556679653-cw7sHS1qdXwTQsfd5Gs0BGoj'
PREFIX = '!'

koalatea = slackclient.SlackClient(BOT_TOKEN)

def mention(user):
    return "<@"+user+">"

def sendMessage(channel, text):
    koalatea.api_call("chat.postMessage", channel=channel, text=text, as_user=True)

def parse_to_event(slack_rtm_output):
    if len(slack_rtm_output) > 0:
        eventType = slack_rtm_output[0]["type"]

        if eventType == "message":
            user = slack_rtm_output[0]["user"]
            channel = text = slack_rtm_output[0]["channel"]
            text = slack_rtm_output[0]["text"]
            event_onMessage(text, user, channel)

def event_onMessage(message, user, channel):
    if message.startswith(PREFIX):
        flag_found = False
        command = message[len(PREFIX):].split(" ")[0].lower()
        arguments = message.split(" ")[1:]
        for cmd in commands:
            if command in cmd["alias"]:
                flag_found = True
                eval(cmd["execute"])
        if not flag_found:
            sendMessage(channel, mention(user) + " : '" + command + "' is not a real command!")
    

if __name__ == "__main__":
    if koalatea.rtm_connect():
        print("KoalaTea is up and running!")
        while True:
            parse_to_event(koalatea.rtm_read())
            time.sleep(1)
        
    else:
        print("Connection Failed!")

