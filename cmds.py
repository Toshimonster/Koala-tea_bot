#(message, user, channel, command, arguments)
#sendMessage(channel, text) ; mention(user);

commands = [
    {
        "name" : "Help",
        "description" : "Gives help on given commands.",
        "hidden" : False,
        "syntax" : "Help {command}",
        "alias" : ["help", "hp"],
        "execute" : """
text = ''
if len(arguments) > 0:
    for cmd in commands:
        if cmd['name'].lower() == arguments[0].lower() or arguments[0].lower() in cmd['alias']:
            text = "*" + cmd['name'] + "*\\n_"
            for alias in cmd['alias']:
                text += alias.title() + ', '
            text = text[:-2]
            text += '_\\n\\n> ' + cmd['description'] + '\\n' + '`' + cmd['syntax'] + '`'
    print(text)
    print("got here")
    sendMessage(channel, text)
else:
    for cmd in commands:
        if cmd['hidden'] != True:
            text += cmd["name"] + '\\n'
    sendMessage(channel, mention(user) + ' Our commands are, as follows;\\n```' + text + '```')
"""
    },
    {
        "name" : "Ping",
        "description" : "Replies 'Pong!' When running.",
        "hidden" : False,
        "syntax" : "Ping",
        "alias" : ['ping', 'test'],
        "execute" : """
sendMessage(channel, mention(user) + ' Pong!')
"""
    },
    {
        "name" : "Tearound",
        "description" : "Starts a 'tearound' - asks everyone what they want, and displays it to the user.",
        "hidden" : False,
        "syntax" : "Tearound",
        "alias" : ['tearound', 'teatime'],
        "execute" : """
global FLAG_TEATIME
global TEATIME_CREATOR
global TEATIME_CHANNEL
global TEATIME_END
FLAG_TEATIME = True
TEATIME_CREATOR = user
TEATIME_CHANNEL = channel
TEATIME_END = time.time() + 60
sendMessage(channel, mention(user) + ' The tea round has begun! It will end in 60 seconds!')
thread = ping_slackRequest(p_msg)
thread.start()
"""
    },
    {
        "name" : "Top",
        "description" : "Shows the top 10 Tea makers, in comparison to the amount of drinks they have ordered.",
        "hidden" : False,
        "syntax" : "Top",
        "alias" : ['leaderboards', 'leaderboard', 'top'],
        "execute" : """
text = str()
sorteddb = sorted(database.data.items(), key=lambda x: tryDivide('(x[1]["drinks"]/x[1]["made"])', x))[:10]
for user in sorteddb:
    text += userInfo(user[0])["name"] + " : Made - " + str(user[1]["made"]) + " ; Requested - " + str(user[1]["drinks"]) + "\\n"
sendMessage(channel, 'Leaderboards are as follows: \\n' + text + '\\n')
"""
    },
    {
        "name" : "Bottom",
        "description" : "Shows the top 10 worst Tea makers, in comparison to the amount of drinks they have ordered.",
        "hidden" : False,
        "syntax" : "Bottom",
        "alias" : ['namenshame', 'nameandshame', 'bottom'],
        "execute" : """
text = str()
sorteddb = sorted(database.data.items(), key=lambda x: tryDivide('(x[1]["made"]/x[1]["drinks"])', x))[:10]
for user in sorteddb:
    text += userInfo(user[0])["name"] + " : Made - " + str(user[1]["made"]) + " ; Requested - " + str(user[1]["drinks"]) + "\\n"
sendMessage(channel, 'Leaderboards are as follows: \\n' + text + '\\n')
"""
    },
    {
        "name" : "Teatypes",
        "description" : "Shows all teatypes, and thier aliases.",
        "hidden" : False,
        "syntax" : "Teatypes",
        "alias" : ['teatype', 'teatypes', 'teavariant', 'teavariants', 'TEAVARIANTS', 'TEATYPES'],
        "execute" : """
text = ""
for drink in teatypes:
    text += drink[0] + " : "
    for thisalias in drink[1]:
        text += thisalias + ", "
    text[:-2]
    text += "\\n"
sendMessage(channel, mention(user) + "\\n" + text)
"""
    },
    {
        "name" : "Covfefe",
        "description" : "What is its meaning.....?",
        "hidden" : True,
        "syntax" : "Covfefe",
        "alias" : ['covfefe'],
        "execute" : """
sendMessage(channel, mention(user) + ' Its a secret to everybody, except the man himself... http://trumpdonald.org')
"""
    },
    {
        "name" : "Shouldent",
        "description" : "Shows somthing impossible.",
        "hidden" : True,
        "syntax" : "Shouldent",
        "alias" : ['shouldent', 'notworking', 'impossible', 'snoop'],
        "execute" : """
sendMessage(channel, mention(user) + ":rr: This shouldn't work, but it does: https://www.youtube.com/watch?v=9w_2JGILUoc")
"""
    },
    {
        "name" : "Running",
        "description" : "Shows somone going vroom",
        "hidden" : True,
        "syntax" : "Running",
        "alias" : ['running'],
        "execute" : """
sendMessage(channel, mention(user) + 'https://i.kinja-img.com/gawker-media/image/upload/s--5Wj0lBIo--/c_scale,f_auto,fl_progressive,q_80,w_800/nomefdcma7s1pctiqaad.gif RUNNING IN THE 90s')
"""
    },
    {
        "name" : "Cat",
        "description" : "Show a random cat.",
        "hidden" : False,
        "syntax" : "Cat",
        "alias" : ["cat", "meow", "cats"],
        "execute" : """
sendMessage(channel, requests.get('http://random.cat/meow').json()["file"])
"""
    },
    {
        "name" : "Gif",
        "description" : "Displays a random gif based on a query.",
        "hidden" : False,
        "syntax" : "Gif {query}",
        "alias" : ["gif", "gifmeh", "animation"],
        "execute" : """
thisrequest = "%20".join(arguments)
thisjson = requests.get("http://api.tenor.com/v1/search?key=LIVDSRZULELA&tag=" + thisrequest + "&limit=10&country=uk").json()
if len(thisjson["results"]) > 0:
    imageurl = random.choice(thisjson["results"])["url"]
    sendMessage(channel, imageurl)
else:
    sendMessage(channel, "Your request was so abstract, noone has posted a gif of it yet!")
"""
    },
    {
        "name" : "Img",
        "description" : "Displays a random img based on a query.",
        "hidden" : False,
        "syntax" : "Img {query}",
        "alias" : ["image", "img"],
        "execute" : """
a = imgur.gallery_search(" ".join(arguments), sort="best")
if len(a) > 0:
    loc_index = random.choice(a)
    print(loc_index.link)
    sendMessage(channel, loc_index.link)
else:
    sendMessage(channel, "Your request was so abstract, noone has posted a image of it yet!")
"""
    }
    
]

