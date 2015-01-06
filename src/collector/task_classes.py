'''
Created on 2014-12-02

@author: Administrator
'''
import logging
import Queue
import socket
import threading
import time
import traceback
import types

from lib import common
from tasks import tasklist

''' Log '''
errlogger = logging.getLogger('error')


###############
### Classes ###
###############

class Task(object):
    '''
    classdocs
    
    resources is a dict of tuple! whick likes [ {"DB":{"user":'root',"password":''}}, ... ]
    '''

    def __init__(self, task=None, resources=tuple(), interval=1, THD_QUEUE=Queue.Queue()):
        '''
        Constructor
        '''
        self._taskMsgType     = task['type']
        self._taskModuleName  = task['module']
        self._taskFuncName    = task['func']
        
        self._interval = interval
       
        self._resources = resources
        
        self._THD_QUEUE = THD_QUEUE
        
        
    def run(self):
        if self._resources is None:
            new_thread = threading.Thread(target=self._task_processor)
            new_thread.daemon = True
            new_thread.start()
        else: 
            for val in self._resources:
                # in a task 
                new_thread = threading.Thread(target=self._task_processor, args=[val])
                new_thread.daemon = True
                new_thread.start()
        
            
    
    def _task_processor(self,resource=None):
        #run task
        taskModlue = __import__(("tasks.%s.%s" % (self._taskMsgType, self._taskModuleName)), globals(), locals(), self._taskFuncName)
        taskFunc = getattr(taskModlue, self._taskFuncName)

        while(True):
            # Sleep first, then run!
            time.sleep(self._interval)
                
            # Run task
            objMsgBody = taskFunc(resource)
            if objMsgBody is None:
                continue
            elif objMsgBody == False:
                errlogger.error("Task function return error, thread exit")
                break
        
            # Make Message
            msgBodyType = type(objMsgBody)
            if msgBodyType == types.DictType:
                ''' type is dict ,direct insert into Queue '''
                objMsg = self._addMsgCommonInfo(objMsgBody, resource)
                self._putMsg2Queue(objMsg)
            elif msgBodyType == types.ListType:
                ''' type is a List of dict, insert each one into Queue '''
                for realObjMsgBody in objMsgBody:
                    objMsg = self._addMsgCommonInfo(realObjMsgBody, resource)
                    self._putMsg2Queue(objMsg)
            
    
    def _addMsgCommonInfo(self, objMsgBody, resource=None):
        objMsg = dict()
        objMsg["type"] = self._taskMsgType
        if resource is None:
            objMsg["from"] = common.getHostName()
        else:
            if resource.has_key('mysql'):
                objMsg["from"] = resource['mysql']['host']
            elif resource.has_key('host'):
                objMsg["from"] = resource['host']['ip']
            else:
                objMsg["from"] = 'Unknown'
        objMsg["collecor"] = common.getHostName()
        objMsg["time"] = common.now()
        objMsg["content"] = objMsgBody
        return objMsg
                
    def _putMsg2Queue(self,objMsg):
        try:
            self._THD_QUEUE.put(objMsg, block=False, timeout=None)
        except Queue.Full:
            errlogger.warning("Thread resource Queue is full")
        except:
            errlogger.exception("Thread resource Queue putting error")
        
        
def runTaskList(THD_QUEUE=Queue.Queue()):
    for taskInfo in tasklist.tasklist:
        interval = taskInfo['interval']
        if taskInfo.has_key('resources'):
            resources=taskInfo['resources']
        else:
            resources=None
        task = Task(task=taskInfo, resources=resources, interval=interval, THD_QUEUE=THD_QUEUE)
        task.run()
     

