
    {
        "alias" : ['teatype', 'teatypes', 'teavariant', 'teavariants', 'TEAVARIANTS', 'TEATYPES'],
        "execute" : """
text = ""
for drink in teatypes:
    text += drink[0] + " : "
      for thisalias in drink[1]:
        text += thisalias + ", "
    text[:-2]
    text += "\n"
""
sendMessage(channel, mention(user) + text)
"""
        }
    

