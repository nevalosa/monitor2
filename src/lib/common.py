'''
Created on 2014-12-22

@author: Administrator
'''
import datetime
import logging
import logging.handlers
import time
import socket

''' Access log path '''
__loggeneral__   = ''
__loggeneral_maxbytes__ = 1
__loggeneral_num__ = 1

''' Error log path '''
__logerror__   = ''
__logerror_maxbytes__ = 1
__logerror_num__ = 2

''' Log Format '''
LOG_FORMAT = '[%(asctime)s, "%(filename)s", line %(lineno)d]\n%(levelname)s: %(message)s'

genLogger = None

''' User Defined '''    
# Common Functions
def init_genlog(path, maxbytes, backupcount, logformat):
    ''' Access log path '''
    global __loggeneral__
    global __loggeneral_maxbytes__
    global __loggeneral_num__

    ''' Log Format '''
    global LOG_FORMAT

    __loggeneral__ = path
    __loggeneral_maxbytes__ = maxbytes
    __loggeneral_num__ = backupcount

    ''' Log Format '''
    LOG_FORMAT = logformat

    global genLogger

    

def init_errlog(path, maxbytes, backupcount, logformat):
    ''' Access log path '''
    global __loggeneral__
    global __loggeneral_maxbytes__
    global __loggeneral_num__

    ''' Log Format '''
    global LOG_FORMAT

    __loggeneral__ = path
    __loggeneral_maxbytes__ = maxbytes
    __loggeneral_num__ = backupcount

    ''' Log Format '''
    LOG_FORMAT = logformat

def log_prepare():
    global __loggeneral__
    global __loggeneral_maxbytes__
    global __loggeneral_num__

#    global genLogger

    loghandler = logging.handlers.RotatingFileHandler(__loggeneral__, maxBytes=__loggeneral_maxbytes__,backupCount=__loggeneral_num__)
    logging.getLogger('general').addHandler(loghandler)


def log():
   
    genLogger = logging.getLogger('general')
    genLogger.error("111")    

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
    errlog(bbb)
