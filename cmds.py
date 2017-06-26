#(message, user, channel, command, arguments)
#sendMessage(channel, text) ; mention(user);

commands = [
    {
        "alias" : ['ping', 'test'],
        "execute" : """
sendMessage(channel, mention(user) + ' Pong!')
"""
    },
    {
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
"""
    },
    {
        "alias" : ['covfefe'],
        "execute" : """
sendMessage(channel, mention(user) + ' Its a secret to everybody, except the man himself... http://trumpdonald.org')
"""
    }

 
]

