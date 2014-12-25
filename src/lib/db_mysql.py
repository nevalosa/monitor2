'''
Created on 2014-12-02

@author: Administrator
'''
import sys
import traceback
import types

from my_global import *

import _mysql
import _mysql_exceptions 

#===============================================================================
# try:
#     import MySQLdb
# except ImportError:
#     exit('This example requires that `MySQLdb` library'
#          ' is installed: \n    yum install MySQL-python\n'
#          'https://pypi.python.org/pypi/MySQL-python/1.2.5'
#          'http://mysql-python.sourceforge.net/MySQLdb.html')
#===============================================================================



DefaultDBCoon = None

def connect(DB_CONFIG=None, user=None, passwd=None, host=None, port=None, db=None):
    '''
    
    '''
    
    try:
        if DB_CONFIG is not None:
            conn = _mysql.connect(user=DB_CONFIG['user'], 
                              passwd=DB_CONFIG['passwd'], 
                              host=DB_CONFIG['host'], 
                              port=DB_CONFIG['port'], 
                              db=DB_CONFIG['db'])
        else:
            conn = _mysql.connect(user=user,
                                passwd=passwd,
                                host=host,
                                port=port,
                                db=db)
    except _mysql_exceptions.Error, e:
        errmsg = "MySQL Error: %d %s" % (e.args[0], e.args[1])
        errlog(errmsg)
        return False
    except:
         traceback.print_exc() 
    
    return conn
      
class Model(object):
    '''
    classdocs
    '''

    def __init__(self, tableName=None, conn=None):
        '''
        Constructor
        Usage: ModelInstance = Model(String tableName , DbConnection conn)
        '''
        
        self._conn  = None
        self._stat  = None
        
        # SQL Variables . Need to be initailize after every query
        self._tableName = tableName
        self._field = None
        self._condition = None
        self._order = None
        self._limit = None
        self._values = None
        
        # Initaize connection
        if conn is None:
            global DefaultDBCoon
            self._conn = DefaultDBCoon
        else:
            self._conn = conn
        
        # Initaize SQL Variables
        self._initailize()
        
        # Test connection
        global DEBUG
        if DEBUG:
            try:
                self._stat = self._conn.stat()
            except:
                traceback.print_exc()
        
    def _initailize(self):
        # SELECT
        self._field = '*'
        self._condition = None
        self._order = None
        self._limit = None
        
        # INSERT
        self._data = None # Dict
        self._insert_id = 0
        
        # INSERT, DELETE, UPDATE
        self._affected_rows = 0
        
        pass
    
    def execute(self, sql):
        '''
        Execute SQL without Return
        '''
        #=======================================================================
        # self._cursor=self._conn.cursor()
        # self._cursor.execute("""SELECT spam, eggs, sausage FROM breakfast
        #   WHERE price < %s""", (max_price,))
        # pass
        #=======================================================================
        result = False
        
        try:    
            print sql
            self._conn.query(sql)
            self._conn.store_result()
            result = True
        except _mysql_exceptions.Error, e:
            errmsg = "MySQL Error: %d %s" % (e.args[0], e.args[1])
            errlog(errmsg)
            result = False
        finally:
            self._initailize()
            
        return result
        
    
    def query(self, sql, maxrows=0, how=1):
        '''
        Query for Select
        '''  
        try:    
            self._conn.query(sql)
            store_result = self._conn.store_result()
            result = store_result.fetch_row(maxrows=maxrows,how=how)
        except _mysql_exceptions.Error, e:
            errmsg = "MySQL Error: %d %s" % (e.args[0], e.args[1])
            errlog(errmsg)
            result = False
        finally:
            self._initailize()
        return result
    
    def where(self, condition=None):
        '''
            Where 
        '''
        realCond = None
        
        if condition is None:
            return self
        
        argsType = type(condition)
        # Direct where string
        if argsType == types.StringType:
            realCond = condition
            pass
        # Cant not use now
        elif argsType == types.DictType: 
            # Convert Dict to String
            pass
        else:
            functionName = sys._getframe().f_code.co_name
            errmsg = "Type of argument 'condition' in %s() should be %s or %s" \
                    % (functionName, types.StringType, types.DictType)
            raise TypeError, errmsg

        # Add Key word 'WHERE' 
        self._condition = realCond
        return self
    
    def field(self, field='*'):
        '''
        Fields
        '''      
        if '*' == field:
            return self
        
        realField = None
        argsType = type(field)
        # Direct Field string
        if argsType == types.StringType:
            realField = field
            pass
        # Cant not use now
        elif argsType == types.DictType: 
            # Convert Dict to String
            pass
        else:
            functionName = sys._getframe().f_code.co_name
            errmsg = "Type of argument 'field' in %s() should be %s or %s" \
                    % (functionName, types.StringType, types.DictType)
            raise TypeError, errmsg
        
        self._field = realField
        return self
    
    def order(self, order):
        '''
        ORDER BY for Select
        '''
        self._order = order
        return self
    
    def limit(self, limit):
        '''
        LIMIT 
        '''
        self._limit = limit
        return self
    
    def find(self):
        '''
        SELECT one row, Return Dict
        '''
        self._limit = 1
        result = self.select()
        if result is None:
            return None
        else:
            return result[0]
    
    def getField(self, field):
        '''
        SELECT , return Dict with key 'field[0]'
        '''
        pass
        
    def select(self):
        '''
        SELECT , reutrn Tuple
        '''
        sql = "SELECT %s FROM %s " \
            % (self._field, self._tableName)
        if self._condition is not None:
            sql = "%s WHERE %s" % (sql, self._condition)
        
        if self._order is not None:
            sql = "%s ORDER BY %s" % (sql, self._order)
        
        if self._limit is not None:
            sql = "%s LIMIT %s" % (sql, self._limit)

        #print sql
        result = self.query(sql)
        try:
            result[0]
        except Exception, e:
            return None
        return result


    def add(self, data=None, replace=False):
        '''
        Insert
        Return :
            Success: 
                return id if id is Auto Increment
                or return True
            Fail:
                return False
            
        Arguments:
            Dict data : {key1:value1, key2:value2, ...}
            Bool replace 
        '''
        # Judge which data to use
        if data is None:
            if self._data is None:
                return False
        else:
            self._data = data
        
        # INSERT or REPLACE
        if True == replace:
            _replace = "REPLACE  "
        else:
            _replace = "INSERT "
        
        # Check Type
        argsType = type(self._data)
        if argsType == types.DictType: 
            # Good,Next Step is Converting Dict to String
            pass
        else:
            functionName = sys._getframe().f_code.co_name
            errmsg = "Type of argument 'data' in %s() should be %s" \
                    % (functionName, types.DictType)
            raise TypeError, errmsg
        
        # sql
        keys = ''
        values = ''

        for (key, val) in self._data.items():
#            print type(val)
            tmpval = _mysql.escape_string(str(val)) 

            if keys != '':
                keys = keys + ','
                values = values + ','
            keys = keys + key
            values = values + "'" + tmpval + "'"
        
        sql = "%s INTO %s(%s) VALUES(%s)" \
            % (_replace, self._tableName, keys, values)

        result = self.execute(sql)
        
        if result: # Execute Succeed
            # Insert ID
            insert_id = self._conn.insert_id()
            if insert_id > 0:   # Primary key is AUTO_INCREMENT (or will be 0)
                return insert_id
        else:   # Execute Failed
            pass
        
        return result
    
    
    def delete(self):
        '''
        DELETE
        Return :
            Success: 
                return affected_rows if affected_rows > 0 
            Fail:
                return False
        '''
        sql = "DELETE FROM %s " \
            % self._tableName
            
        if self._condition is not None:
            sql = "%s WHERE %s" % (sql, self._condition)
            
        if self._limit is not None:
            sql = "%s LIMIT %s" % (sql, self._limit)

        #print sql
        result = self.execute(sql)
        
        if result: # Execute Succeed
            # Insert ID
            affected_rows = self._conn.affected_rows()
            if affected_rows > 0:   # Primary key is AUTO_INCREMENT (or will be 0)
                return affected_rows
        else:   # Execute Failed
            pass
        
        return result
        
    def save(self, data):
        '''
        UPDATE
        Return :
            Success: 
                return affected_rows if affected_rows > 0 
            Fail:
                return False
            
        Arguments:
            Dict data : {key1:value1, key2:value2, ...}
        '''
        # Judge which data to use
        if data is None:
            if self._data is None:
                return False
        else:
            self._data = data
        
        # Check Type
        argsType = type(self._data)
        if argsType == types.DictType: 
            # Convert Dict to String
            pass
        else:
            functionName = sys._getframe().f_code.co_name
            errmsg = "Type of argument 'data' in %s() should be %s" \
                    % (functionName, types.DictType)
            raise TypeError, errmsg
        
        # sql
        sets = ''

        for (key, val) in self._data.items():
#            print type(val)
            tmpval = _mysql.escape_string(str(val)) 
            if sets != '':
                sets = sets + ','
            sets = sets + key + "='" + tmpval + "'" 
        
        sql = "UPDATE %s SET %s" \
            % (self._tableName,sets )
        
        if self._condition is not None:
            sql = "%s WHERE %s" % (sql, self._condition)
            
        if self._limit is not None:
            sql = "%s LIMIT %s" % (sql, self._limit)
            
        result = self.execute(sql)
        
        if result: # Execute Succeed
            # Insert ID
            affected_rows = self._conn.affected_rows()
            if affected_rows > 0:   # Primary key is AUTO_INCREMENT (or will be 0)
                return affected_rows
        else:   # Execute Failed
            pass
        
        return result
    
    

# Examples
if __name__ == '__main__':
    
    # Create Connection
    DefaultDBCoon = _mysql.connect(user='admin', passwd='admin', 
                                    host='192.168.126.13', port=3306, db='test')

    # Create Model    
    M = Model('mytest')
    
    #Select
    print 'SELECT:'
    print '  ' ,M.field('id, value').where('id>1').order('id asc').limit(3).select()
    
    print 'GetField:'
    print '  ' ,M.getField('id, k')
    
    print 'FIND:'
    print '  ' ,M.find()
        
    #Insert
    print 'INSERT:'
    data1 = {'id':1,
             'value':'aaa'}
    data2 = {'id':2,
             'value':'aaa'}
    data3 = {'id':3,
             'value':'aaa'}
    print '  id is:' ,M.add(data1,True)
    print '  id is:' ,M.add(data2,True)
    print '  id is:' ,M.add(data3,True)
    
    # Delete
    print 'DELETE:'
    print '  delete rows:' ,M.where('id=1').limit(1).delete()
    
    # Update
    print 'UPDATE:'
    data = {'id':2,
             'value':'bbb'}
    print '  update rows' ,M.where('id=2').save(data)
