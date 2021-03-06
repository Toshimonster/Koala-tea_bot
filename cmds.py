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
    if text != '':
        sendMessage(channel, text)
    else:
        sendMessage(channel, "Could not find command `" + arguments[0] + "`!")
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
        "name" : "Screenfetch",
        "description" : "Gives infomation of the server, running Koala-tea",
        "hidden" : False,
        "syntax" : "Screenfetch",
        "alias" : ["screenfetch", "status"],
        "execute" : """
screenfetch_output = subprocess.check_output(['screenfetch', '-N',  '-D', 'arch']).decode('utf-8')
sendMessage(channel, '```' + screenfetch_output + '```')
"""
    },
    {
	"name" : "Reboot",
	"description" : "Reboots the bot's server",
	"hidden" : False,
	"syntax" : "Reboot",
	"alias" : ["reboot", "restart"],
	"execute" : """
sendMessage(channel, mention(user) + ' : Rebooting...')
subprocess.check_output(['reboot'])
"""
    },
    {
        "name" : "Tearound",
        "description" : "Starts a 'tearound' - asks everyone what they want, and displays it to the user.",
        "hidden" : False,
        "syntax" : "Tearound {time in seconds}",
        "alias" : ['tearound', 'teatime'],
        "execute" : """
global FLAG_TEATIME
global TEATIME_CREATOR
global TEATIME_CHANNEL
global TEATIME_END
global TEATIME_LENGTH
global TEATIME_TEAS
global TEATIME_CANCELED
global TEATIME_LENGTH_OG
global thread
global TEATIME_SUBSCRIPTIONS
if not FLAG_TEATIME:
    TEATIME_TEAS = []
    FLAG_TEATIME = True
    if len(arguments) > 0:
        try:
            TEATIME_LENGTH = eval(arguments[0])
        except:
            TEATIME_LENGTH = TEATIME_LENGTH_OG
    else:
        TEATIME_LENGTH = TEATIME_LENGTH_OG
    TEATIME_CREATOR = user
    TEATIME_CHANNEL = channel
    
    sendMessage(channel, '<!channel> : The tea round has begun! It will end in ' + str(TEATIME_LENGTH) + ' seconds!')
    for subscription in TEATIME_SUBSCRIPTIONS:
        TEATIME_TEAS.append([subscription[1], subscription[0]])
        sendMessage(channel, mention(subscription[0]) + ' : The subscripted ' + subscription[1] + ' has been added!')

    TEATIME_END = time.time() + TEATIME_LENGTH
    TEATIME_CANCELED = False
    thread = ping_slackRequest(p_msg)
    thread.start()
else:
    sendMessage(channel, mention(user) + ' : A tea round is already running! `!cancel` it first!')
"""
    },
    {
        "name" : "Peronitime",
        "description" : "Starts a 'Peroni Time' - asks everyone what they want, and displays it to the user.",
        "hidden" : False,
        "syntax" : "Peronitime {time in seconds}",
        "alias" : ['peronitime', 'fabledcountdownclock'],
        "execute" : """
if time.localtime().tm_hour < 16 or datetime.datetime.now().strftime("\%a") != "Friday":
    sendMessage(channel, mention(user) + ' : *GET BACK TO WORK!*')
else:
    global P_FLAG_TEATIME
    global P_TEATIME_CREATOR
    global P_TEATIME_CHANNEL
    global P_TEATIME_END
    global P_TEATIME_LENGTH
    global P_TEATIME_TEAS
    global P_TEATIME_CANCELED
    global P_TEATIME_LENGTH_OG
    global P_thread
    if not P_FLAG_TEATIME:
    	P_TEATIME_TEAS = []
    	P_FLAG_TEATIME = True
    	if len(arguments) > 0:
            try:
            	P_TEATIME_LENGTH = eval(arguments[0])
            except:
            	P_TEATIME_LENGTH = TEATIME_LENGTH_OG
    	else:
            P_TEATIME_LENGTH = TEATIME_LENGTH_OG
    	P_TEATIME_CREATOR = user
    	P_TEATIME_CHANNEL = channel
    	P_TEATIME_END = time.time() + P_TEATIME_LENGTH
    	P_TEATIME_CANCELED = False
    	sendMessage(channel, 'https://www.gifgif.io/QNMlcP.gif\\n<!channel> : The peroni round has begun! It will end in ' + str(P_TEATIME_LENGTH) + ' seconds!')
    	P_thread = ping_slackRequest_peroni(p_msg)
    	P_thread.start()
    else:
    	sendMessage(channel, mention(user) + ' : A peroni round is already running! `!cancel` it first!')

"""
    },
    {
        "name" : "Top",
        "description" : "Shows the top Tea makers, in comparison to the amount of drinks they have ordered.",
        "hidden" : False,
        "syntax" : "Top",
        "alias" : ['leaderboards', 'leaderboard', 'top'],
        "execute" : """
sendMessage(channel, 'Generating leaderboards...')
text = str()
sorteddb = sorted(database.data.items(), key=lambda x: tryDivide('(x[1]["drinks"]/x[1]["made"])', x))
for user in sorteddb:
    text += userInfo(user[0])["name"] + " : Made - " + str(user[1]["made"]) + " ; Requested - " + str(user[1]["drinks"]) + "\\n"
sendMessage(channel, 'Leaderboards are as follows: \\n```' + text + '```\\n')
"""
    },
    {
        "name" : "Bottom",
        "description" : "Shows the worst Tea makers, in comparison to the amount of drinks they have ordered.",
        "hidden" : False,
        "syntax" : "Bottom",
        "alias" : ['namenshame', 'nameandshame', 'bottom'],
        "execute" : """
sendMessage(channel, 'Generating leaderboards...')
text = str()
sorteddb = sorted(database.data.items(), key=lambda x: tryDivide('(x[1]["made"]/x[1]["drinks"])', x))
for user in sorteddb:
    text += userInfo(user[0])["name"] + " : Made - " + str(user[1]["made"]) + " ; Requested - " + str(user[1]["drinks"]) + "\\n"
sendMessage(channel, 'Leaderboards are as follows: \\n```' + text + '```\\n')
"""
    },
    {
        "name" : "Teatypes",
        "description" : "Shows all teatypes, and thier aliases.",
        "hidden" : False,
        "syntax" : "Teatypes",
        "alias" : ['teatype', 'teatypes', 'teavariant', 'teavariants'],
        "execute" : """
text = ""
for drink in teatypes:
    text += drink[0] + " : "
    for thisalias in drink[1]:
        text += thisalias + ", "
    text[:-2]
    text += "\\n"
sendMessage(channel, mention(user) + "\\n```" + text + "```\\n \\n *If you dont see your drink here, you can do `custom {name}` during a tearound!*")
"""
    },
    {
        "name" : "Peronitypes",
        "description" : "Shows all peronitypes, and thier aliases.",
        "hidden" : False,
        "syntax" : "Peronitypes",
        "alias" : ['peronitype', 'peronitypes', 'peronivariant', 'peronivariants'],
        "execute" : """
text = ""
for drink in peronitypes:
    text += drink[0] + " : "
    for thisalias in drink[1]:
        text += thisalias + ", "
    text[:-2]
    text += "\\n"
sendMessage(channel, mention(user) + "\\n```" + text + "```\\n \\n *If you dont see your drink here, you can do `custom {name}` during a peroniround!*")
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
        "name" : "Sekrit Dokuments",
        "description" : "This will show true russian sekrit dokuments cover.",
        "hidden" : True,
        "syntax" : "Sekrit",
        "alias" : ['sekrit', 'secret', 'dokuments'],
        "execute" : """
sendMessage(channel, mention(user) + http://cdn-live.warthunder.com/uploads/f4/9b8f9593601926568cc98120ded45b1dc588f3_lq/Sekrit%20dokuments%20wip.PNG Here are sekrit dokuments for you.
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
        "name" : "RandomUser",
        "description" : "Produces a random user, to be used as tests in programs.",
        "hidden" : False,
        "syntax" : "RandomUser",
        "alias" : ["randomuser", "randuser", "ruser"],
        "execute" : """
user = requests.get('https://randomuser.me/api/?nat=gb&noinfo&format=json').json()["results"][0]
attatchment = {
    "author_name" : user["name"]["title"].title() + " " + user["name"]["first"].title() + " " + user["name"]["last"].title(),
    "image_url" : user["picture"]["thumbnail"],
    "title" : user["email"],
    "fields" : [
        {
            "title": "Login details",
            "value": user["login"]["username"] + " : " + user["login"]["password"]
        },
        {
            "title": "Location",
            "value": user["location"]["state"] + ", " + user["location"]["city"] + ", " + user["location"]["street"] + ", " + user["location"]["postcode"]
        },
        {
            "title": "General Info",
            "value": "DOB : " + user["dob"] + "\\nPHONE : (H) " + user["phone"] + " (M) " + user["cell"]
        }
    ],
    "footer": "Gender : " + user["gender"]
}
koalatea.api_call("chat.postMessage", channel=channel, text="Random User", as_user=True, attachments=[attatchment])
"""
    },
    {
        "name" : "Cancel",
        "description" : "Cancels a tearound",
        "hidden" : False,
        "syntax" : "Cancel",
        "alias" : ["cancel"],
        "execute" : """
sendMessage(channel, "A teatime has to be running to do that!")
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
thisjson = requests.get("http://api.tenor.com/v1/search?key=" + TENOR_KEY + "&tag=" + thisrequest + "&limit=10&country=uk").json()
if len(thisjson["results"]) > 0:
    imageurl = random.choice(thisjson["results"])["url"]
    sendMessage(channel, imageurl)
else:
    sendMessage(channel, "Your request was so abstract, noone has posted a gif of it yet!")
"""
    },
    {
        "name" : "Tea",
        "description" : "Displays a random gif of 'teas'",
        "hidden" : False,
        "syntax" : "Tea",
        "alias" : ["teameme", "tea"],
        "execute" : """
thisjson = requests.get("http://api.tenor.com/v1/search?key=" + TENOR_KEY + "&tag=" + "tea" + "&limit=10&country=uk").json()
if len(thisjson["results"]) > 0:
    imageurl = random.choice(thisjson["results"])["url"]
    sendMessage(channel, imageurl)
else:
    sendMessage(channel, "No teas ;-;")
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
    sendMessage(channel, loc_index.link)
else:
    sendMessage(channel, "Your request was so abstract, noone has posted a image of it yet!")
"""
    },
    {
        "name" : "Id",
        "description" : "Gets the id of a user",
        "hidden" : True,
        "syntax" : "Id {username}",
        "alias" : ["id"],
        "execute" : """
if len(arguments) > 0:
    this_id = getId(arguments[0])
    if this_id == False:
        sendMessage(channel, "Could not find user with the username : " + arguments[0])
    else:
        sendMessage(channel, "The user's ID is " + this_id)
else:
    sendMessage(channel, "Your ID is " + user)
"""
    },
    {
        "name" : "Excel",
        "description" : "Gives a excel sheet of the users",
        "hidden" : False,
        "syntax" : "Excel",
        "alias" : ["excel", "xlsx"],
        "execute" : """
createXcel()
data = ''
with open('Data.xlsx', 'rb') as file:
    data = file.read()
upload_file('Leaderboard.xlsx', data, channel)
"""
    },
    {
        "name" : "Error",
        "description" : "Gives the log of the program",
        "hidden" : False,
        "syntax" : "Error",
        "alias" : ["error", "logs"],
        "execute" : """
data = ''
with open('logs.log', 'r') as file:
    data = file.read()
upload_file('logs.log', data, channel)
"""
    },
    {
        "name" : "CatPlaceholder",
        "description" : "Gives a cat image based on a height and width.",
        "hidden" : False,
        "syntax" : "CatPlaceholder {width} {height}",
        "alias" : ["catplaceholder", "placeholders", "catify"],
        "execute" : """
content = requests.get("https://placekitten.com/{}/{}".format(arguments[0], arguments[1])).content
if not upload_file('placeholder.jpg', content , channel):
    sendMessage(channel, "No placeholder found!")
"""
    },
    {
    	"name" : "Execute",
	"description" : "Runs a command on the bot's server. _Please dont forkbomb me.... please..._",
	"hidden" : False,
	"syntax" : "Execute {command}",
	"alias" : ["execute", "evaluate"],
	"execute" : """
try:
    verbose(user + " : executed : " + " ".join(arguments))
    result = os.popen(" ".join(arguments)).read()
    verbose(result)
    if not upload_file('result.exec', result, channel):
       sendMessage(channel, "ERROR! Please check !error") 
except Exception as e:
    verbose(e)
    sendMessage(channel, "ERROR! Please check !error")
"""
   },
   {
       "name" : "Subcription",
       "description" : "Subscribes to a certain teatype, to automatically add yourself to a tearound.",
       "hidden" : False,
       "syntax" : "Subscription {teatype} {hours}",
       "alias" : ["subscribe", "subscription"],
       "execute" : """
global TEATIME_SUBSCRIPTION
if len(arguments) == 2:
    teatype = checkTea(arguments[0])
    if teatype != False:
        if float(arguments[1]) > 0 and float(arguments[1]) <= 3:
            try:
                subscription = [user, teatype, (time.time() + (float(arguments[1]) * (60*60))), channel]
                TEATIME_SUBSCRIPTIONS.append(subscription)
                sendMessage(channel, "Subscribed " + mention(user) + " with " + teatype + " for " + arguments[1] + " hours!")
            except:
                sendMessage(channel, mention(user) + " : Length of subscription must be a number!")
        else:
            sendMessage(channel, mention(user) + " : Length of subscription must be more than `0` but less than `3`!")
    else:
        sendMessage(channel, mention(user) + " : Unknown Teatype!")
"""
    },
    {
	"name" : "Unsubscribe",
	"description" : "Unsubscribes all current subscriptions for yourself",
	"hidden" : False,
	"syntax" : "Usubscribe",
	"alias" : ["unsubscribe"],
	"execute" : """
global TEATIME_SUBSCRIPTIONS
this_arr = TEATIME_SUBSCRIPTIONS
num_of_rm = 0
for index, subscription in enumerate(TEATIME_SUBSCRIPTIONS):
    if subscription[0] == user:
	num_of_rm += 1
	this_arr[index] = "Del Me"
for i in range(num_of_rm):
    this_arr.pop(this_arr.index("Del Me"))

TEATIME_SUBSCRIPTIONS = this_arr
sendMessage(channel, mention(user) + ' : Removed all your subscriptions!')

"""
    },
    {
	"name" : "Clearlogs",
	"description" : "It says it on the tin!",
	"hidden" : False,
	"syntax" : "Clearlogs",
	"alias" : ["clearlogs", "logclear"],
	"execute" : """
ret = subprocess.check_output(['rm', '/root/../logs.log'])
sendMessage(channel, "Removed all logs! \\n")
verbose(user + ' Cleared all logs')
"""
    }
]
