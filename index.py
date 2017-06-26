import slackclient
BOT_TOKEN = 'xoxb-203343544195-g7R8xTWZqqvZppkCdWnYuClr'

koalatea = slackclient.SlackClient(BOT_TOKEN)


koalatea.send(channel, text)

koalatea.users
