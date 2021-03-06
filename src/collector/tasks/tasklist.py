'''
Created on 2014-12-02

@author: Administrator
'''

tasklist = [
            
    # User #
    {
        "enable"   : True,
        "comment"  : "Collect: Number of Users,including register and unregister(guest) and so on.", 
        "type"     : "APP_RECORD",
        "module"   : "projectXuser", 
        "func"     : "apprec_user",
        "interval" : 30,
        "resources": [
            {
                "mysql" : { 
                    "user"  : "dba", 
                    "passwd": "123456", 
                    "host"  : "127.0.0.1", 
                    "port"  : 3306, 
                    "db"    : "user"
                },
                "redis" : { 
                    "host"  : "127.0.0.1", 
                    "port"  : 6379, 
                    "db"    : 0 
                }
            }
        ],
    },
    
    {
        "enable"   : True,
        "comment"  :"Calculate Average Data from 'apprec_user' to speedup long term chart display", 
        "type"     :"APP_RECORD",
        "module"   :"projectXuser", 
        "func"     :"apprec_user_avg",
        "interval" :86400,
        "resources":[
            {
                "mysql" : { 
                    "user"  : "admin", 
                    "passwd": "admin", 
                    "host"  : "127.0.0.1", 
                    "port"  : 3306, 
                    "db"    : "monitor"
                }
            }
        ],
    },
            
    {
        "enable"   : True,
        "comment"  :"Analysis: Daily max or min user", 
        "type"     :"APP_RECORD",
        "module"   :"projectXuser", 
        "func"     :"apprec_user_statistics",
        "interval" :86400,
        "resources":[
            {
                "mysql" : { 
                    "user"  : "admin", 
                    "passwd": "admin", 
                    "host"  : "127.0.0.1", 
                    "port"  : 3306, 
                    "db"    : "monitor"
                }
            }
        ],
    },
    
    
    # Conference #
    {
        "enable"   : True,
        "comment"  :"Collect: Total amount of conference", 
        "type"     :"APP_RECORD",
        "module"   :"projectXconference", 
        "func"     :"apprec_conf",
        "interval" :300,
        "resources":[
            {
                "mysql" : { 
                    "user"  : "dba", 
                    "passwd": "123456", 
                    "host"  : "127.0.0.1", 
                    "port"  : 3306, 
                    "db"    : "conf"
                },
                "redis" : { 
                    "host"  : "127.0.0.1", 
                    "port"  : 6379, 
                    "db"    : 0 
                }
            }
        ],
    },

    {
        "enable"   : True,
        "comment"  :"Collect: Daily statistics including max/min number of conference", 
        "type"     :"APP_RECORD",
        "module"   :"projectXconference", 
        "func"     :"apprec_conf_statistics",
        "interval" :86400,
        "resources":[
            {
                "mysql" : { 
                    "user"  : "dba", 
                    "passwd": "123456", 
                    "host"  : "127.0.0.1", 
                    "port"  : 3306, 
                    "db"    : "conf"
                },
            }
        ],
    },

    # Files #
    {
        "enable"   : True,
        "comment"  :"Collect: Number of daily created files",
        "type"     :"APP_RECORD",
        "module"   :"projectXfile", 
        "func"     :"conf_file_daily_num",
        "interval" :86400,
        "resources":[
                {
                    "db" : { 
                        "user"  : "dba", 
                        "passwd": "123456", 
                        "host"  : "127.0.0.1", 
                        "port"  : 3306, 
                        "db"    : "file"
                    }
                }
            ], 
    },

]
            
