'''
Created on 2014-12-22

@author: Administrator
'''

import logging
import redis

from lib import db_mysql
from lib import common

def apprec_user(resource=None):
    '''
        Get Number of Users
    '''
    TARGET_TABLE='apprec_user'
    
    DBCoon = db_mysql.connect(user=resource['mysql']['user'], 
                              passwd=resource['mysql']['passwd'], 
                              host=resource['mysql']['host'], 
                              port=resource['mysql']['port'], 
                              db=resource['mysql']['db'])
    
    RedisCoon = redis.StrictRedis(host=resource['redis']['host'], 
                                  port=resource['redis']['port'], 
                                  db=6)

    # Get Data    
    mUser = db_mysql.Model('user',DBCoon)
    dataResult = mUser.field("count(*) AS num").where("1=1").find()
    if dataResult == False:
        return False
    webRegisterNum = dataResult['num']
    
    mGuest = db_mysql.Model('user_guest',DBCoon)
    dataResult = mGuest.field("count(*) AS num").where("1=1").find()
    if dataResult == False:
        return False
    webGuestNum = dataResult['num']
    
    try:
        dataResult = RedisCoon.info('keyspace')
        sipOnlineNum = dataResult['db11']['keys']
    except:
        logging.exception("Redis operation error")
        return False
    
    
    
    # Set Value
    values = dict()
    values['type'] = 0
    values['real_time'] = common.now()
    values['register_user'] = webRegisterNum
    values['guest_user'] = webGuestNum
    values['sip_online_user'] = sipOnlineNum
    
    # fill message body
    msgBody = common.fillMsgData(TARGET_TABLE, values)
    return msgBody

def apprec_user_avg(resource=None):
    '''
        Calculate Average Data from 'apprec_user' to speedup long term chart display
        -- Connect With Monitor --
    '''
    TARGET_TABLE='apprec_user'
    DBCoon = db_mysql.connect(user=resource['mysql']['user'], 
                              passwd=resource['mysql']['passwd'], 
                              host=resource['mysql']['host'], 
                              port=resource['mysql']['port'], 
                              db=resource['mysql']['db'])

    yesterday = common.lastday()
   
    # Get Data
    mUser = db_mysql.Model('apprec_user',DBCoon)
    
    # check last day statistics data
    strWhere = "type=2 and real_time='%s 23:59:59'" % (yesterday)
    dataResult = mUser.field("id").where(strWhere).find()
    # SQL error
    if dataResult == False:
        return False
    if dataResult is not None:  # data already exists
        return None

    # Get last day normal data
    strWhere = "type=0 and real_time>'%s 00:00:00' and real_time<='%s 23:59:59'" % (yesterday,yesterday)
    dataResult = mUser.where(strWhere).select()
    # SQL error
    if dataResult == False:
        return False
    # No data
    if dataResult is None:
        return None

    registerSum = 0
    guestSum    = 0 
    sipOnlineSum= 0
    for val in dataResult:
        registerSum += int(val['register_user'])
        guestSum += int(val['guest_user'])
        sipOnlineSum += int(val['sip_online_user'])
        
    registerAvg = int(registerSum / len(dataResult)) 
    guestAvg    = int(guestSum / len(dataResult)) 
    sipOnlineAvg= int(sipOnlineSum / len(dataResult)) 
    
    # Set Value
    values = dict()
    values['type'] = 2
    values['real_time'] = "%s 23:59:59" % yesterday
    values['register_user'] = registerAvg
    values['guest_user'] = guestAvg
    values['sip_online_user'] = sipOnlineAvg
    
    # fill message body
    msgBody = common.fillMsgData(TARGET_TABLE, values)
    return msgBody
    
    

def apprec_user_statistics(resource=None):
    ''' 
        Daily Usr Datastatistics
        -- Connect With Monitor --
    '''
    TARGET_TABLE='apprec_user_statistics'
    
    DBCoon = db_mysql.connect(user=resource['mysql']['user'], 
                              passwd=resource['mysql']['passwd'], 
                              host=resource['mysql']['host'], 
                              port=resource['mysql']['port'], 
                              db=resource['mysql']['db'])

    yesterday = common.lastday()
   
    # Get Data
    mUser = db_mysql.Model('apprec_user',DBCoon)
    
    # check last day statistics data
    strWhere = "type=2 and real_time='%s 23:59:59'" % (yesterday)
    dataResult = mUser.field("id").where(strWhere).find()
    # SQL error
    if dataResult == False:
        return False
    if dataResult is not None:  # data already exists
        return None

    # Get last day normal data
    strWhere = "type=0 and real_time>'%s 00:00:00' and real_time<='%s 23:59:59'" % (yesterday,yesterday)
    dataResult = mUser.where(strWhere).select()
    # SQL error
    if dataResult == False:
        return False
    # No data
    if dataResult is None:
        return None

    MAX_SIP = 0
    MIN_SIP = dataResult[0]['sip_online_user']
    MAX_WEB = 0
    MIN_WEB = dataResult[0]['web_online_user']
    MAX_PC = 0
    MIN_PC = dataResult[0]['pc_online_user']
    for val in dataResult:
        if MAX_SIP < int(val['sip_online_user']):
            MAX_SIP = int(val['sip_online_user'])
        if MIN_SIP > int(val['sip_online_user']):
            MIN_SIP = int(val['sip_online_user'])
            
        if MAX_WEB < int(val['web_online_user']):
            MAX_WEB = int(val['web_online_user'])
        if MIN_WEB > int(val['web_online_user']):
            MIN_WEB = int(val['web_online_user'])
            
        if MAX_PC < int(val['pc_online_user']):
            MAX_PC = int(val['pc_online_user'])
        if MIN_PC > int(val['pc_online_user']):
            MIN_PC = int(val['pc_online_user'])
    
    # Set Value
    values = dict()
    values['type'] = 2
    values['real_time'] = "%s 23:59:59" % yesterday
    values['max_sip'] = MAX_SIP
    values['min_sip'] = MIN_SIP
    values['max_web'] = MAX_WEB
    values['min_web'] = MIN_WEB
    values['max_pc'] = MAX_PC
    values['min_pc'] = MIN_PC
    
    # fill message body
    msgBody = common.fillMsgData(TARGET_TABLE, values)
    return msgBody
   
def apprec_user_rt_statistics(resource=None):
    pass
