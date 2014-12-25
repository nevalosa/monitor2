'''
Created on 2014-12-22

@author: Administrator
'''

from lib import db_mysql
from lib import common


DBCoon = db_mysql.connect(user='admin', passwd='admin', 
                        host='192.168.126.8', port=3306, db='gscf_user')

'''
Get web register num
'''
def web_register_num():
    TARGET_TABLE='apprec_web_user_num'

    # Get Data    
    mUser = db_mysql.Model('user',DBCoon)
    dataResult = mUser.field("count(*) AS num").where("1=1").find()
    webRegisterNum = dataResult['num']
    
    mGuest = db_mysql.Model('user_guest',DBCoon)
    dataResult = mGuest.field("count(*) AS num").where("1=1").find()
    webGuestNum = dataResult['num']
    
    # Set Value
    values = dict()
    values['type'] = 0
    values['real_time'] = common.now()
    values['register_user'] = webRegisterNum
    values['guest_user'] = webGuestNum
    
    # fill message body
    msgBody = common.fillMsgBody(TARGET_TABLE, values)
    return msgBody


'''
Get Daily Sip Max user and Min user
'''
def daily_sip_register():
    TARGET_TABLE='apprec_sip_register_num'
    
     # Set Value
    values = dict()
    values['type'] = 1
    values['real_time'] = common.now()
#    values['register_user'] = w
#    values['guest_user'] = webGuestNum
    
    # fill message body
    msgBody = common.fillMsgBody(TARGET_TABLE, values)
    return msgBody
   


