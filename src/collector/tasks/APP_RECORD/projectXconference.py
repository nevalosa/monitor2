'''
Created on 2014-12-29

@author: Administrator
'''

from lib import db_mysql
from lib import common


def conf_daliy_num():
    '''
        Get daliy and effective num of yesterday conference 

    '''
    yesterday = common.lastday()

    TARGET_TABLE='apprec_conf_daily_num'

    DBCoon = db_mysql.connect(user='gsdba', passwd='yhnmkoert', 
                        host='172.172.172.18', port=3306, db='gscf_conf')

    ''' Get Data '''
    # daily conf #
    mConf = db_mysql.Model('conf_info',DBCoon)
    strWhere = "state >0 and start_time>'%s 00:00:00' and start_time<='%s 23:59:59'" % (yesterday,yesterday)
    dataResult = mConf.field("count(*) AS num").where(strWhere).find()
    if dataResult == False:
        return False
    confNum = dataResult['num']

    # daliy effective conf #
    strWhere = "state >0 and start_time>'%s 00:00:00' and start_time<='%s 23:59:59' and duration>10" % (yesterday,yesterday)
    dataResult = mConf.field("count(*) AS num").where(strWhere).find()
    if dataResult == False:
        return False
    confEffectiveNum = dataResult['num']
   
    ''' Set Value '''
    values = dict()
    values['type'] = 0
    values['real_time'] = "%s 23:59:59" % yesterday
    values['conf_num'] = confNum
    values['conf_effective_num'] = confEffectiveNum
    
    ''' fill message body '''
    msgBody = common.fillMsgData(TARGET_TABLE, values)
    return msgBody



