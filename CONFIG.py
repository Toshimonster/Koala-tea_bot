import os

settings = {

    #The prefix used to run each command
    "PREFIX" : "!",

    #The time given during a tearound
    "TEATIME_LENGTH" : 180,

    #The bot token for the bot
    "SLACK_BOT_TOKEN" : os.getenv('SLACK_BOT_TOKEN'),

    #The imgur api infomation for the !img command
    "IMGUR_BOT_ID" : os.getenv('IMGUR_BOT_ID'),

    #The imgur api infomation for the !img command
    "IMGUR_BOT_SECRET" : os.getenv('IMGUR_BOT_SECRET'),

    #The tenor api infomation for the !gif command
    "TENOR_KEY" : os.getenv('TENOR_KEY')

}
