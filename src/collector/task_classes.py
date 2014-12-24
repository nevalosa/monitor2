'''
Created on 2014-12-02

@author: Administrator
'''

import Queue
import socket
import threading
import traceback

from lib import common
from tasks import tasklist

class Task(object):
    '''
    classdocs
    '''

    def __init__(self, task=None, resource=dict(), interval=1, THD_QUEUE=Queue.Queue()):
        '''
        Constructor
        '''
        self._taskMsgType     = task['type']
        self._taskModuleName  = task['module']
        self._taskFuncName    = task['func']
        
        self._interval = interval
        
        self._resource = resource
        
        self._THD_QUEUE = THD_QUEUE
        
        
    def run(self):
        for val in self._resource:
            # in a task 
            new_thread = threading.Thread(target=self._task_processor)
            new_thread.daemon = True
            new_thread.start()
        
            
    
    def _task_processor(self):
        #run task
        taskModlue = __import__(("tasks.%s.%s" % (self._taskMsgType, self._taskModuleName)), globals(), locals(), self._taskFuncName)
        #print dir(taskModlue)
        taskFunc = getattr(taskModlue, self._taskFuncName)

        objMsgBody = taskFunc()
        
        # Make Message
        objMsg = dict()
        objMsg["type"] = self._taskMsgType
        objMsg["from"] = common.getHostName()
        objMsg["time"] = common.now()
        objMsg["content"] = objMsgBody
        
        try:
            self._THD_QUEUE.put(objMsg, block=False, timeout=None)
        except Queue.Full:
            print "Quere is full." #dev#
        except:
            traceback.print_exc() 
        pass

        
        
def runTaskList(THD_QUEUE=Queue.Queue()):
    for taskInfo in tasklist.tasklist:
        task = Task(task=taskInfo, resource=['192.168.126.8'], interval=10, THD_QUEUE=THD_QUEUE)
        task.run()
     
     
