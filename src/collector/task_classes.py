'''
Created on 2014-12-02

@author: Administrator
'''

import Queue
import threading
import traceback

class Task(object):
    '''
    classdocs
    '''

    def __init__(self, taskName=None, resource=tuple(), interval=1, THD_QUEUE=Queue.Queue()):
        '''
        Constructor
        '''
        self._taskName = taskName
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
        from tasks.APP_RECORD.max_sip_register_num import max_sip_register_num
        (msgType, objMsgBody) = max_sip_register_num()
        
        objMsg = dict()
        objMsg["type"] = msgType
        objMsg["from"] = ""
        objMsg["time"] = "2014-12-04 12:12:15"
        objMsg["content"] = objMsgBody
        
        try:
            self._THD_QUEUE.put(objMsg, block=False, timeout=None)
        except Queue.Full:
            print "Quere is full." #dev#
        except:
            traceback.print_exc() 
        pass
    
def runTaskList(THD_QUEUE=Queue.Queue()):
     task1 = Task(taskName="max_sip_register_num", resource=["a","b"] , interval=0, THD_QUEUE=THD_QUEUE)
     task1.run()
     
     
