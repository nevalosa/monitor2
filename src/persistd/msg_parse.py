'''
Created on 2014-11-28

@author: Administrator
'''
import json
import logging

from lib import db_mysql

''' Log '''
errlogger = logging.getLogger('error')


#################
### Functions ###
#################
def getMessageType(resource):
    try:
        jsonObj = json.loads(str(resource))
    except  Exception,e:
        errlogger.exception("Json parse error")
        return False
    
    try:
        messageType = jsonObj['type']
    except Exception,e:
        errmsg = "Type does not exist in the Json Message"
        errlogger.exception("Json object property 'type' need")
        return False
    return messageType
    

def msg_push_parse(thd):
    '''
    msg_push_parse Function
    Receive phone push messages ,and send push to phone
    '''
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
    Receive data messages ,and analysis&save data
    '''
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
        errlogger.exception("Json Parse Error")
        return False
    
    

def dispatch_message(messageType, thd):
    '''
    dispatch_message Function
    '''
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
    parse_message(thd)
    #
    #end thread(thd)
    pass

if __name__ == '__main__':
    pass
