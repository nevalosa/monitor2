'''
Created on 2014-12-22

@author: Administrator
'''
import time


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
    
def msg_add_basic_info(msgBody=None):
    msg = '''
    
    ''' % msgBody 
    pass

# Dev Code
if __name__ == '__main__':
    aaa = 123
    bbb =  "%s wolegeca" % aaa 
    errlog(bbb)