'''
Created on 2014-12-29

@author: Administrator
'''

import logging
import redis

from lib import db_mysql
from lib import common


def apprec_conf(resource=None):
    '''
        Get Total amount of conference
    '''
    TARGET_TABLE='apprec_conference'
    
    DBCoon = db_mysql.connect(user=resource['mysql']['user'], 
                              passwd=resource['mysql']['passwd'], 
                              host=resource['mysql']['host'], 
                              port=resource['mysql']['port'], 
                              db=resource['mysql']['db'])
    
    RedisCoon = redis.StrictRedis(host=resource['redis']['host'], 
                                  port=resource['redis']['port'], 
                                  db=resource['redis']['db'])
    # Get Data    
    mConf = db_mysql.Model('conf_info',DBCoon)
    dataResult = mConf.field("count(*) AS num").where("1=1").find()
    if dataResult == False:
        return False
    conf_total = dataResult['num']
    
    try:
        dataResult = RedisCoon.info('keyspace')
        sipOnlineNum = dataResult['db6']['keys']
    except:
        logging.exception("Redis operation error")
        return False
    
    # Set Value
    values = dict()
    values['type'] = 0
    values['real_time'] = common.now()
    values['total'] = conf_total
    values['sip_online_conf'] = sipOnlineNum
    
    # fill message body
    msgBody = common.fillMsgData(TARGET_TABLE, values)
    return msgBody

def apprec_conf_statistics(resource=None):
    '''
        Get daliy and effective num of yesterday conference 

    '''
    yesterday = common.lastday()

    TARGET_TABLE='apprec_conference_statistics'

    DBCoon = db_mysql.connect(user=resource['mysql']['user'], 
                              passwd=resource['mysql']['passwd'], 
                              host=resource['mysql']['host'], 
                              port=resource['mysql']['port'], 
                              db=resource['mysql']['db'])

    ''' Get Data '''
    # Yesterdat daily conf #
    mConf = db_mysql.Model('conf_info',DBCoon)
    strWhere = "state >0 and start_time>'%s 00:00:00' and start_time<='%s 23:59:59'" % (yesterday,yesterday)
    dataResult = mConf.field("count(*) AS num").where(strWhere).find()
    if dataResult == False:
        return False
    yesterdayConfNum = dataResult['num']

    # daliy effective conf #
    strWhere = "state >0 and start_time>'%s 00:00:00' and start_time<='%s 23:59:59' and duration>10" % (yesterday,yesterday)
    dataResult = mConf.field("count(*) AS num").where(strWhere).find()
    if dataResult == False:
        return False
    yesterdayConfEffectiveNum = dataResult['num']
   
    ''' Set Value '''
    values = dict()
    values['type'] = 2
    values['real_time'] = "%s 23:59:59" % yesterday
    values['conf_num'] = yesterdayConfNum
    values['conf_effective_num'] = yesterdayConfEffectiveNum
    
    ''' fill message body '''
    msgBody = common.fillMsgData(TARGET_TABLE, values)
    return msgBody



def apprec_conf_rt_statistics(resource=None):
    pass
