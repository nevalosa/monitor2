'''
Created on 2014-12-04

@author: Administrator
'''
import os
import sys
import time

if __name__ == '__main__':
    from proton import *

    user = os.getenv('ACTIVEMQ_USER') or 'admin'
    password = os.getenv('ACTIVEMQ_PASSWORD') or 'password'
    host = os.getenv('ACTIVEMQ_HOST') or '127.0.0.1'
    port = int(os.getenv('ACTIVEMQ_PORT') or 5672)
    destination = sys.argv[1:2] or ['topic://event']
    destination = destination[0]
    
    msg = Message()
    mng = Messenger()
    mng.password=password
    mng.start()
    mng.subscribe("amqp://%s@%s:%d/%s"%(user, host, port, destination))
    
    count = 0 
    start = time.time()
    while True:
      print '###Step: recv###'
      mng.recv(1)
      while mng.incoming:
        mng.get(msg)
        print '###Step: get###'
    
        if msg.body=="SHUTDOWN":
          diff = time.time() - start
          print 'Received %d frames in %f seconds' % (count, diff)
          exit(0)
        else:
          print msg.body
          if count==0:
            start = time.time()
          count+=1
          if count % 1000 == 0:
            print 'Received %d messages.' % (count)
    
    mng.stop()