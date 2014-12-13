'''
Created on 2014-12-03

@author: Administrator
'''
import time

# DB Config
DB_CONFIG = {'user'  : 'admin', 
             'passwd': 'admin',
             'host'  : '192.168.126.8', 
             'port'  : 3306, 
             'db'    : 'monitor'}

DB_CONFIG_USER={}

# Default Golable System Variables
''' pid file path '''
__pidfile__     = '/tmp/monitor.pid'

''' Access log path '''
__loggeneral__   = None #'/var/log/my_general.log'

''' Error log path '''
__logerror__   = None #'/var/log/my_error.log'

''' Number of concurrency threads '''
__thread_concurrency__ = 2

''' Max queue size of received messages from MQ Server, Zero means unlimit '''
__mq_queue_size__ = 0 


''' Debug Switch '''
DEBUG = False 

''' Thread resources Queue '''
THD_QUEUE = None



# Common Functions
def _output2tty(message):
    print message
    
def _output2log(message, logpath):
    pass

def generallog(message, redirct=None):
    '''
    Print general log to tty Or log
    '''
    if redirct is None:
        if __loggeneral__ is None: # write to tty
            _output2tty(message)
            pass
        else: # write to log
            _output2log(message, __loggeneral__)
            pass
    elif 'tty' == redirct: # write to tty
        _output2tty(message)
        pass
    elif 'log' == redirct: # write to log
        _output2log(message, __loggeneral__)
        pass
    else:
        return

def errlog(message, redirct=None):
    '''
    Print general log to tty Or log
    '''
    message = "[%s]Error: %s.\n" % (time.strftime('%Y-%m-%d %H:%M:%S'), message)
    
    if redirct is None:
        if __logerror__ is None: # write to tty
            _output2tty(message)
            pass
        else: # write to log
            _output2log(message, __logerror__)
            pass
    elif 'tty' == redirct: # write to tty
        _output2tty(message)
        pass
    elif 'log' == redirct: # write to log
        _output2log(message, __logerror__)
        pass
    else:
        return
    


# Dev Code
if __name__ == '__main__':
    aaa = 123
    bbb =  "%s wolegeca" % aaa 
    errlog(bbb)