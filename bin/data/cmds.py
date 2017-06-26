def execute(msg):
    print(msg)

a = [
    {
        "name"    : "help",
        "alias"   : ["h", "helpme"],
        "execute" : execute
    }
]

msg = input()
if a[0]["name"] == msg:
    a[0]["execute"](msg)

