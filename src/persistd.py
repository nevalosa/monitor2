"""
Usage:
    ./persistd --help
    ./persistd [options] [ACTION]
         
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
import logging
import logging.handlers
import os
import platform
import Queue
import sys
import threading
import time

# My Libs
from lib import common
from lib import db_mysql
from persistd import msg_parse
from persistd import thd_classes

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
    

########################################
### Default Golable System Variables ###
########################################
''' Default Database Config '''
DB_CONFIG = {'user'  : 'admin', 
             'passwd': 'admin',
             'host'  : '192.168.126.8', 
             'port'  : 3306, 
             'db'    : 'monitor'}

''' pid file path '''
__pidfile__     = '/tmp/monitor.pid'

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

''' Number of concurrency threads '''
__thread_concurrency__ = 2

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

def check_os():
    ''' Unsupported os '''
    running_system = platform.system()
    if ('Linux' != running_system) and ('Windows' != running_system):
        errlogger.errorl("Unsupported Operation System")
        _shutdown()
        sys.exit(0)

def server_init():
    '''
    Initailize server environment
    '''

    # Store thread resources
    global THD_QUEUE 
    THD_QUEUE = Queue.Queue(__mq_queue_size__) 
    

def create_new_thread():
    '''
    Consume a Quere Resource 'THD' for message processing,
    Use Quere to keep resource threading safe
    '''
    global THD_QUEUE

    # Database 
    MySQLCoon = db_mysql.connect(DB_CONFIG)
    if False == MySQLCoon:
        sys.exit(2)
    
    while(True):
        # Init
        thd = dict()
        
        # Consume Queue
        try:
            thd = THD_QUEUE.get(block=True, timeout=None)
        except Queue.Empty:
            errlogger.warning("Queue is empty")
            continue
        except:
            errlogger.exception("Queue getting error")
            
        # Prepare thd
        thd.setMySQLCoon(MySQLCoon)
        # Real Process 
        msg_parse.handle_one_message(thd)
        # Queue Recycle
        THD_QUEUE.task_done()
        pass


def handle_messagequeue_messags():
    '''
    Handle the MQ messages
    '''
    global THD_QUEUE
    
    errlogger.info("Building %d threads for works." % __thread_concurrency__)
    for i in range(__thread_concurrency__):
        new_thread = threading.Thread(target=create_new_thread)
        new_thread.daemon = True
        new_thread.start()
    
    errlogger.info("Waiting for message from MQ...")    
    if "Linux" == platform.system():
        ''' Linux: use proton amqp '''
        from lib import amqp_consumer
        amqpConsumer = amqp_consumer.Consumer()
        while(True):
            # Get Msg From MQ
            message = amqpConsumer.getMsg()
            errlogger.debug("Received message:\n%s" % message)
            thd = thd_classes.THD(resource=message)
            
            # Put resourc into Process Queue 
            try:
                THD_QUEUE.put(thd, block=False, timeout=None)
            except Queue.Full:
                errlogger.warning("Thread resource Queue is full")
                continue
            except:
                errlogger.exception("Thread resource Queue putting error")
        pass
                
    elif 'Windows' == platform.system():
        ''' Windows: without proton ''' 
        num = 0 #dev
        while(True):
            # Get Msg From MQ
            #dev#message = amqpCnsumer.getMsg()
            message = '''
{
    "type": "APP_RECORD",
    "content": {
        "obj_name":"apprec_user_sip_num",
        "values": {
            "type":0,
            "register_type_id":0,
            "num":108
        }
    },
    "from": "",
    "time": "2014-12-04 12:12:15"
}
        
            ''' 
            errlogger.debug("Received message -\n%s" % message)
            thd = thd_classes.THD(resource=message)
            # Put resourc into Process Queue 
            try:
                THD_QUEUE.put(thd, block=False, timeout=None)
            except Queue.Full:
                errlogger.warning("Thread resource Queue is full")
                continue
            except:
                errlogger.exception("Thread resource Queue putting error")

            num+=1 #dev 
            if num>0:#dev
                break #dev
        pass
    
    # block until all tasks are done
    THD_QUEUE.join()
   
 
def main(args=None):
    ''' Main Function'''    
    try:     
        #Base config
        PROGRAM_NAME = os.path.basename(sys.argv[0])
        
        # Server Initalize
        server_init()
        
        # Handle MQ Messages
        handle_messagequeue_messags()
        
        # Last time for the thread to finish their work 
        time.sleep(1)
        pass
    
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        errlogger.info("User Interrupt Catched")
        pass
    
    except Exception, e:
        errlogger.exception("Fatal error exiting")
        #indent = len(PROGRAM_NAME) * " "
        #sys.stderr.write(PROGRAM_NAME + ": " + repr(e) + "\n")
        #sys.stderr.write(indent + "  for help use --help")
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

def load_ini_config():
    '''Load the initail config file '''
    pass


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
                error='''Usage:
    ./persistd --help
    ./persistd [options] start|stop|restart|status
'''
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

    # Check System
    check_os()
        
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

    
