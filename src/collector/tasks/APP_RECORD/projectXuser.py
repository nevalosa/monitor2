'''
Created on 2014-12-22

@author: Administrator
'''

from lib import db_mysql
from lib import common


def web_register_num():
    '''
        Get web register num
    '''
    TARGET_TABLE='apprec_user_web_num'
    DBCoon = db_mysql.connect(user='admin', passwd='admin', 
                        host='192.168.126.8', port=3306, db='gscf_user')

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
    
    # Set Value
    values = dict()
    values['type'] = 0
    values['real_time'] = common.now()
    values['register_user'] = webRegisterNum
    values['guest_user'] = webGuestNum
    
    # fill message body
    msgBody = common.fillMsgData(TARGET_TABLE, values)
    return msgBody


def daily_sip_register():
    ''' 
        Get Daily Sip Max user and Min user 
    '''
    TARGET_TABLE='apprec_user_sip_num'
    DBCoon = db_mysql.connect(user='admin', passwd='admin', 
                        host='192.168.126.8', port=3306, db='monitor')
    MAX_NUM = 0
    MIN_NUM = 0

    yesterday = common.lastday()
   
    # Get Data    
    mUser = db_mysql.Model('apprec_user_sip_num',DBCoon)
    
    # check last day statistics data
    strWhere = "type=21 and real_time>'%s 00:00:00' and real_time<='%s 23:59:59'" % (yesterday,yesterday)
    dataResult = mUser.field("id").where(strWhere).find()
    # SQL error
    if dataResult == False:
        return False
    if dataResult is not None:  # data already exists
        return None

    # Get last day normal data
    strWhere = "type=0 and real_time>'%s 00:00:00' and real_time<='%s 23:59:59'" % (yesterday,yesterday)
    dataResult = mUser.field('num').where(strWhere).select()
    # SQL error
    if dataResult == False:
        return False
    # No data
    if dataResult is None:
        return None
    
    MIN_NUM = dataResult[0]['num']
    for val in dataResult:
        if MAX_NUM < int(val['num']):
            MAX_NUM = int(val['num'])
        if MIN_NUM > int(val['num']):
            MIN_NUM = int(val['num'])
    
    # Set Value
    msgBodyList = list()

    values = dict()
    values['type'] = 21
    values['real_time'] = "%s 23:59:59" % yesterday
    values['num'] = MIN_NUM
    msgBody = common.fillMsgData(TARGET_TABLE, values)
    msgBodyList.append(msgBody)
    
    values = dict()
    values['type'] = 22
    values['real_time'] = "%s 23:59:59" % yesterday
    values['num'] = MAX_NUM
    msgBody = common.fillMsgData(TARGET_TABLE, values)
    msgBodyList.append(msgBody)
    
    return msgBodyList
   

