'''
Created on 2014-12-02

@author: Administrator
'''

import Queue
import socket
import threading
import time
import traceback
import types

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
       
        if resource is None:
            self._resource = [0]
        else: 
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

        while(True):
            # Sleep first, then run!
            time.sleep(self._interval)
                
            # Run task
            objMsgBody = taskFunc()
            
            if objMsgBody is None:
                continue
            elif objMsgBody == False:
                print "task error, thread exit"
                break
        
            # Make Message
            msgBodyType = type(objMsgBody)
            if msgBodyType == types.DictType:
                ''' type is dict ,direct insert into Queue '''
                objMsg = self._addMsgCommonInfo(objMsgBody)
                self._putMsg2Queue(objMsg)
            elif msgBodyType == types.ListType:
                ''' type is a List of dict, insert each one into Queue '''
                for realObjMsgBody in objMsgBody:
                    objMsg = self._addMsgCommonInfo(realObjMsgBody)
                    self._putMsg2Queue(objMsg)
            
        #=======================================================================
        #     objMsg = dict()
        #     objMsg["type"] = self._taskMsgType
        #     objMsg["from"] = common.getHostName()
        #     objMsg["time"] = common.now()
        #     objMsg["content"] = objMsgBody
        # 
        #     try:
        #         self._THD_QUEUE.put(objMsg, block=False, timeout=None)
        #     except Queue.Full:
        #         print "Quere is full." #dev#
        #     except:
        #         traceback.print_exc()
        #=======================================================================
    
    def _addMsgCommonInfo(self,objMsgBody):
        objMsg = dict()
        objMsg["type"] = self._taskMsgType
        objMsg["from"] = common.getHostName()
        objMsg["time"] = common.now()
        objMsg["content"] = objMsgBody
        return objMsg
                
    def _putMsg2Queue(self,objMsg):
        try:
            self._THD_QUEUE.put(objMsg, block=False, timeout=None)
        except Queue.Full:
            print "Quere is full." #dev#
        except:
            traceback.print_exc()
        
        
def runTaskList(THD_QUEUE=Queue.Queue()):
    for taskInfo in tasklist.tasklist:
        interval = taskInfo['interval']
        if taskInfo.has_key('resource'):
            resource=taskInfo['resource']
        else:
            resource=None
        task = Task(task=taskInfo, resource=resource, interval=interval, THD_QUEUE=THD_QUEUE)
        task.run()
     
     
