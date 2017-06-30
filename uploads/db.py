import json

class db(object):
    
    def __init__(self, file):
        self.file = file

        try:
            with open(self.file, 'r') as ThisFile:
                self.data = json.loads(ThisFile.read())
        except:
            with open(self.file, 'w+') as ThisFile:
                ThisFile.write('{}')

    def write(self):
        with open(self.file, 'w') as ThisFile:
            ThisFile.write(json.dumps(self.data, indent=4, sort_keys=True))
