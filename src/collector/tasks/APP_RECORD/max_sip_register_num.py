'''
Created on 2014-12-22

@author: Administrator
'''

from lib import db_mysql

DBCoon = db_mysql.connect(user='admin', passwd='admin', 
                        host='192.168.126.8', port=3306, db='monitor')

'''
Get daily max SIP register num
'''
def max_sip_register_num():

    TARGET_TABLE = "apprec_sip_register_num"
    msgBody = dict()
    msgBody["obj_name"] = "apprec_sip_register_num"
    msgBody["values"] = dict()
    msgBody["values"]['type'] = 0
    msgBody['values']['num'] = 18
    msgBody['values']['register_type_id'] = 28

    # Create Model    
    mSipRegisterNum = db_mysql.Model('apprec_sip_register_num')
    
    
    
    return ("APP_RECORD", msgBody)