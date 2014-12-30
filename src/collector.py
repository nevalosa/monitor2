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
import os
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
    


# Default Golable System Variables
''' pid file path '''
__pidfile__     = '/tmp/collector.pid'
''' Access log path '''
__logaccess__   = '/var/log/collector.log'
''' Number of concurrency threads '''
__thread_concurrency__ = 1
''' Max queue size of received messages from MQ Server, Zero means unlimit '''
__mq_queue_size__ = 0 

''' Debug Switch '''
DEBUG = False 
''' Thread resources Queue '''
THD_QUEUE = None


# Functions
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
            print "Queue is empty" #dev#
            continue
        except:
            traceback.print_exc() 
   
        # send msg to MQ
        if DEBUG:
            print msg
            pass
        else:
            from lib import amqp_producer
            amqpProductor = amqp_producer.Productor()
            # Convert Dict Msg to Json String
            jSonStrMsg = json.dumps(msg)
            # Send Msg to MQ
            print jSonStrMsg
            amqpProductor.sendMsg(jSonStrMsg)
        
        # Queue Recycle
        THD_QUEUE.task_done()
        pass
 
    # block until all tasks are done
    THD_QUEUE.join()
   
 
def main(args=None):
    ''' Main Function'''
    
    #print(args)
    
    try:
        # Setup argument parser
        print "I'm the master threads(Main.py)." #dev#
        
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
        
        print ("User Interrupt Catched.") #dev#
        return 0
    except Exception, e:
        
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2
    
    finally:
        pass
  

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
     
    # Real Main Func in Daemon
    if DEBUG:
        main(args)
    else:
        from lib import daemonize
        daemon = daemonize.Daemonize(pidfile=__pidfile__, action=main, args=args)
        if 'start'== args['ACTION']:
            daemon.start()
        elif 'stop' == args['ACTION']:
            daemon.stop()
        elif 'restart' == args['ACTION']:
            daemon.restart()

    sys.exit(0)

    
