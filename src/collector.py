"""
Usage:
    ./collector --help
    ./collector [options] [ACTION]
         
Arguments:
  ACTION        Program control command, available options:
                start(DEFAULT) | stop | restart | status
                
Options:
  -h --help     Show this help message and exit
  -v            Verbose mode.
  
  --debug        Run in front and output debug log.
  --defaults-file=#
                Only read default options from the given file #. 
  --log-access=#
  --log-error=#
  --pid-file=#
"""

# System libs
import json
import logging
import logging.handlers
import os
import platform
import Queue
import sys
import threading
import time
import traceback


# My Libs
from lib import db_mysql
from lib import my_global
from lib import msg_parse
from collector import task_classes

# Third libs
try:
    import docopt
except ImportError:
    exit('This example requires that `docopt` arguments-validation library'
         ' is installed: \n    pip install docopt==0.6.1\n'
         'https://github.com/docopt/docopt')
    
try:
    import schema
except ImportError:
    exit('This example requires that `schema` data-validation library'
         ' is installed: \n    pip install schema\n'
         'https://github.com/halst/schema')
    
try:
    import redis
except ImportError:
    exit('This example requires that `redis` interface to the Redis key-value store library'
         ' is installed: \n    pip install redis\n'
         'https://github.com/andymccurdy/redis-py')
    


# Default Golable System Variables
''' pid file path '''
__pidfile__     = '/tmp/collector.pid'

''' Access log path '''
__loggeneral__   = 'logs/general.log'
__loggeneral_maxbytes__ = 100*1024*1024
__loggeneral_num__ = 2

''' Error log path '''
__logerror__   = 'logs/error.log'
__logerror_maxbytes__ = 100*1024*1024
__logerror_num__ = 2

''' Log Format '''
LOG_FORMAT = '[%(asctime)s, "%(filename)s", line %(lineno)d] %(levelname)s: %(message)s'
#LOG_FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

''' Max queue size of received messages from MQ Server, Zero means unlimit '''
__mq_queue_size__ = 0 

''' Debug Switch '''
DEBUG = False 

#########################
### Do not modify !!! ###
#########################
''' Program Infomation '''
PROGRAM_NAME = None

''' Thread resources Queue '''
THD_QUEUE = None

''' Log '''
errlogger = logging.getLogger('error')
__loglevel__ = logging.DEBUG



#################
### Functions ###
#################
def log_init():
    ''' log ''' 
    # log: CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET #
    logFormatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    
    if DEBUG:
        __loglevel__ = logging.DEBUG
    else:
        __loglevel__ = logging.INFO

    # Add error log handler 
    errlogger.setLevel(logging.DEBUG)

    fileHandler = logging.handlers.RotatingFileHandler( \
        __logerror__, mode='a', maxBytes=__logerror_maxbytes__, \
        backupCount=__logerror_num__, encoding='utf8', delay=0)
    fileHandler.setLevel(__loglevel__)
    fileHandler.setFormatter(logFormatter)

    errlogger.addHandler(fileHandler)
    
    # Add console log handler 
    console = logging.StreamHandler()
    console.setLevel(__loglevel__)
    console.setFormatter(logFormatter)
    
    errlogger.addHandler(console)
    
def server_init():
    '''
    Initailize server environment
    '''
    # Store thread resources
    global THD_QUEUE 
    THD_QUEUE = Queue.Queue(__mq_queue_size__) 

def handle_collecting_tasks():
    '''
    Handle the collecting tasks
    '''

    # run tasks and add msg to the Queue
    task_classes.runTaskList(THD_QUEUE)

    # Send Message    
    while(True):
        # Init
        msg = dict()
        
        # Consume Queue
        try:
            msg = THD_QUEUE.get(block=True, timeout=None)
        except Queue.Empty:
            errlogger.warning("Queue is empty")
            continue
        except:
            traceback.print_exc() 
   
        # send msg to MQ
        
        if "Linux" == platform.system():
            from lib import amqp_producer
            amqpProductor = amqp_producer.Productor()
            # Convert Dict Msg to Json String
            jSonStrMsg = json.dumps(msg)
            # Send Msg to MQ
            errlogger.debug(jSonStrMsg)
            amqpProductor.sendMsg(jSonStrMsg)
        elif 'Windows' == platform.system():
            print msg
            pass
        
        # Queue Recycle
        THD_QUEUE.task_done()
        pass
 
    # block until all tasks are done
    THD_QUEUE.join()
   
 
def main(args=None):
    ''' Main Function'''
    try:
        #Base config
        program_name = os.path.basename(sys.argv[0])
        
        # Server Initalize
        server_init()
        
        # Collect Data & Send MQ Messages
        handle_collecting_tasks()
        
        # Last time for the thread to finish their work 
        time.sleep(1)
        return 0
    
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        
        errlogger.info("User Interrupt Catched")
        pass
     
    except Exception, e:
        
        errlogger.exception("Fatal error exiting")
        pass
    
    finally:
        _shutdown()
        sys.exit(2)
        
def _shutdown():
    try:
        pf = file(__pidfile__, 'r')
        pid = int(pf.read().strip())
        pf.close()
    except:
        pid = None
        
    if os.path.exists(__pidfile__):
        os.remove(self.pidfile)
        
    errlogger.info("Daemon from pid file %s ended\n\n\n\n" % __pidfile__)
    
    return 0
  

if __name__ == '__main__':
    ''' 
    Parse the arguments
    
    '''
    args = docopt.docopt(__doc__)
    
    # Set default arguments
    if args['--defaults-file'] is None:
        args['--defaults-file'] = 'persistd.cnf'
    
    if args['--log-access'] is None:
        args['--log-access'] = False

    if args['--log-error'] is None:
        args['--log-error'] = False
        pass

    #if args['--pid-file'] is None:
    #    args['--pid-file'] = False
    
    # Arguments checking
    schemaValidate = schema.Schema({
        schema.Optional('ACTION'): 
            schema.And(
                str, schema.Use(str.lower), 
                lambda s: s in ('start', 'stop', 'restart', 'status'), 
                error='Action should be in start|stop|restart|status'
            ),
        '--debug':
            schema.And(
                bool,
                error='Option \'--debug\' shoud be instance of bool'
            ), 
        '--defaults-file': 
            schema.And(
                str,
                error='Option \'--defaults-file\' shoud be instance of str'
            ),
        '--help': 
            schema.And(
                bool,
                error='Option \'--help\' shoud be instance of str'
            ),
        '--log-access': 
            schema.Or(
                object,
                error='Option \'--log-access\' shoud be instance of str'
            ),
        '--log-error': 
            schema.And(
                object,
                error='Option \'--log-error\' shoud be instance of str'
            ),
        '--pid-file': 
            schema.And(
                object,
                error='Option \'--pid-file\' shoud be instance of str'
            ),
        '-v': 
            schema.And(
                bool,
                error='Option \'-v\' shoud be instance of str'
            ),
        })
    
    try:
        args = schemaValidate.validate(args)
    except schema.SchemaError as e:
        exit(e)
        
    # Set Global System variables
    if True == args['--debug']:
        DEBUG = True
     
    # log 
    log_init()
    errlogger.info("%sing daemon from %s" % \
        (args['ACTION'][0].upper() + args['ACTION'][1:], os.getcwd()))   
     
    # Real Main Func in Daemon
    if "Linux" == platform.system():
        from lib import daemonize
        daemon = daemonize.Daemonize(pidfile=__pidfile__, action=main, args=args)
        if 'start'== args['ACTION']:
            daemon.start()
        elif 'stop' == args['ACTION']:
            daemon.stop()
        elif 'restart' == args['ACTION']:
            daemon.restart()
    elif "Windows" == platform.system():
        main(args)

    sys.exit(0)

    
