'''
Created on 2014-12-29

@author: Administrator
'''

from lib import db_mysql
from lib import common


def conf_file_daily_num():
    '''
        Get daliy file num 
        Just yesterday because today is not finished
    '''
    yesterday = common.lastday()

    TARGET_TABLE='apprec_file_daily_num'

    DBCoon = db_mysql.connect(user='gsdba', passwd='yhnmkoert', 
                        host='172.172.172.18', port=3306, db='gscf_file')

    ''' Get Data '''
    # daily file #
    mFile = db_mysql.Model('file_conf_info',DBCoon)
    strWhere = "create_time>'%s 00:00:00' and create_time<='%s 23:59:59'" % (yesterday,yesterday)
    dataResult = mFile.field("count(*) AS num").where(strWhere).find()
    if dataResult == False:
        return False
    fileNum = dataResult['num']

    # daliy effective conf #
    strWhere = "type=2 and create_time>'%s 00:00:00' and create_time<='%s 23:59:59'" % (yesterday,yesterday)
    dataResult = mFile.field("count(*) AS num").where(strWhere).find()
    if dataResult == False:
        return False
    fileVideoNum = dataResult['num']
   
    ''' Set Value '''
    values = dict()
    values['type'] = 0
    values['real_time'] = "%s 23:59:59" % yesterday
    values['file_num'] = fileNum
    values['file_video_num'] = fileVideoNum
    
    ''' fill message body '''
    msgBody = common.fillMsgData(TARGET_TABLE, values)
    return msgBody



