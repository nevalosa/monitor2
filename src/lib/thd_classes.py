'''
Created on 2014-12-02

@author: Administrator
'''

class THD(object):
    '''
    classdocs
    '''

    def __init__(self, resource=None):
        '''
        Constructor
        '''
        self._resource = resource
        self._currentThread = None
        
    def setThreadInfo(self, currentThread=None):
        '''
        Set Thread Info 
        '''
        self._currentThread = currentThread
        
    def setMySQLCoon(self, coon):
        self._mysqlCoon = coon
        
    def getMySQLCoon(self):
        return self._mysqlCoon
    
    def getResource(self):
        return self._resource
        
    
        