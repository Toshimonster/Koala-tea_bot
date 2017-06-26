import slackclient
BOT_TOKEN = 'Token'

koalatea = slackclient.SlackClient(BOT_TOKEN)


koalatea.send(channel, text)

koalatea.users
