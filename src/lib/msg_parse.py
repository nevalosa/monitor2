'''
Created on 2014-11-28

@author: Administrator
'''
import _mysql
import db_mysql

def msg_push_parse(thd):
    '''
    msg_push_parse Function
    '''
    print "I'm the msg push parse function(lib/msg_parse.py)."
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
    print "I'm the msg_data_parse function(lib/msg_parse.py)."
    # detail parse
    datatype = 'user count'
    if 'user count' == datatype:
        #do something
        pass
    else:
        pass
    

def dispatch_message(messageType, thd):
    '''
    dispatch_message Function
    '''
    print "I'm the dispatch_message function(lib/msg_parse.py)."
    if   'PUSH' == messageType:
        pass
    elif 'DATA' == messageType:
        msg_data_parse(thd)
        pass
    elif 'ALERT' == messageType:
        pass
    else:
        pass

def parse_message(thd):
    '''
    parse_message Function
    '''
    print "I'm the parse_message function(lib/msg_parse.py)."
    
    print thd._resource
    
    # Get message type
    messageType = 'PUSH'
    messageType = 'DATA'
    messageType = 'ALERT'
    
    dispatch_message(messageType, thd)
    pass

def handle_one_message(thd):
    '''
    handle one message
    '''
    print "I'm the handle one message function(lib/msg_parse.py)."
    parse_message(thd)
    #
    #end thread(thd)
    pass

if __name__ == '__main__':
    pass