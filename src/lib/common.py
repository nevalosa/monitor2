'''
Created on 2014-12-22

@author: Administrator
'''
import datetime
import logging
import time
import socket

''' Log '''
errlogger = logging.getLogger('error')


''' User Defined '''    
# Common Functions
    
def fillMsgData(objName, values):
    msgBody = dict()
    msgBody["obj_name"] = objName
    msgBody["values"] = values
    return msgBody

''' System '''    
def now():
    return time.strftime('%Y-%m-%d %H:%M:%S')

def lastday():
    today = datetime.date.today() 
    yesterday = today - datetime.timedelta(days=1)
    return yesterday

def getHostName():
    return socket.gethostname()

def getHostIP():
    return socket.gethostbyname(socket.gethostname())


# Dev Code
if __name__ == '__main__':
    aaa = 123
    bbb =  "%s wolegeca" % aaa 
