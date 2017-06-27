import time
from threading import Thread
a = 1

class worker(Thread):
    def run(self):
        for x in range(0,11):
            print(a)
            time.sleep(1)

class waiter(Thread):
    def run(self):
        for x in range(100,103):
            print(a)
            time.sleep(5)

def run():
    worker().start()
    waiter().start()
