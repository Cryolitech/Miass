import random
import threading
import time
def foo(x, s):    
    time.sleep(s)
    print ("%s %s %s" % (threading.current_thread(), x, s))

for x in range(4):
    threading.Thread(target=foo, args=(x, random.random())).start()