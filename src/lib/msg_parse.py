'''
Created on 2014-11-28

@author: Administrator
'''
import db_mysql
import json
import logging

from my_global import *

errlogger = logging.getLogger('error')
def testlog():
    errlogger.info('parse')


def getMessageType(resource):
    try:
        jsonObj = json.loads(str(resource))
    except  Exception,e:
        errmsg = "Message is not valid json"
        errlog(errmsg)
        return False
    
    try:
        messageType = jsonObj['type']
    except Exception,e:
        errmsg = "Type does not exist in the Json Message"
        errlog(errmsg)
        return False
    return messageType
    

def msg_push_parse(thd):
    '''
    msg_push_parse Function
    '''
    print "I'm the msg push parse function(lib/msg_parse.py)." #dev#
    # detail parse
    datatype = 'user count'
    if 'user count' == datatype:
        #do something
        pass
    else:
        pass

def msg_data_parse(thd):
    '''
    msg_data_parse Function
    '''
    print "I'm the msg_data_parse function(lib/msg_parse.py)." #dev#
    # detail parse
    datatype = 'user count'
    if 'user count' == datatype:
        #do something
        pass
    else:
        pass
    
def msg_apprec_parse(thd):
    '''
    msg_data_parse Function
    '''
    print "I'm the msg_data_parse function(lib/msg_parse.py)." #dev#
    # detail parse
    jsonObj = json.loads(str(thd.getResource()))
    
    try:
        # Get Message Body
        msgContent = jsonObj['content']
        # New Table ORM
        model = db_mysql.Model(msgContent['obj_name'],thd.getMySQLCoon())
        # <Dict>msgContent['values'] As value
        model.add(msgContent['values'], True)
    except Exception,e:
        errmsg = "Json Parse Error (%s)" % e
        errlog(errmsg)
        return False
    
    

def dispatch_message(messageType, thd):
    '''
    dispatch_message Function
    '''
    print "I'm the dispatch_message function(lib/msg_parse.py)." #dev#
    if   'PUSH' == messageType:
        pass
    elif 'DATA' == messageType:
        pass
    elif 'ALERT' == messageType:
        pass
    elif 'APP_RECORD' == messageType:
        msg_apprec_parse(thd)
        pass
    else:
        pass

def parse_message(thd):
    '''
    parse_message Function
    '''
    print "I'm the parse_message function(lib/msg_parse.py)." #dev#
    
    print thd._resource #dev#
    
    # Get message type
    messageType = getMessageType(thd.getResource())
    #messageType = 'PUSH'
    #messageType = 'DATA'
    #messageType = 'ALERT'
    if False == messageType:
        return False
        
    dispatch_message(messageType, thd)
    pass

def handle_one_message(thd):
    '''
    handle one message
    '''
    print "I'm the handle one message function(lib/msg_parse.py)." #dev#
    parse_message(thd)
    #
    #end thread(thd)
    pass

if __name__ == '__main__':
    pass
