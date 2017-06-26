#(message, user, channel, command, arguments)
#sendMessage(channel, text) ; mention(user);

commands = [
    {
        "alias" : ['ping', 'test'],
        "execute" : """
sendMessage(channel, mention(user) + ' Pong!')
"""
    }


    
]

