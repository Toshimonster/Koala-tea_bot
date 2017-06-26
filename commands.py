tearound = [
    {
        "alias" : ['!tearound', '/tearound', '!Tearound', '/Tearound'],
        "execute" : """
sendMessage(channel, mention(user) + ' The tea round has begun! It will end in 60 seconds!')
FLAG_TEATIME = True
TEATIME_CREATOR = user
TEATIME_CHANNEL = channel
TEATIME_END = time.time() + 60
"""
        }
    ]

