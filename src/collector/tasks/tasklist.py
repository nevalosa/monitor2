'''
Created on 2014-12-02

@author: Administrator
'''

tasklist = [
            
    # User #
    {
        "comment"  :"Collect: Number of Users,including register and unregister(guest) and so on.", 
        "type"     :"APP_RECORD",
        "module"   :"projectXuser", 
        "func"     :"apprec_user",
        "interval" :30,
        "resources":[
            {
                "mysql" : { 
                    "user"  : "gsdba", 
                    "passwd": "yhnmkoert", 
                    "host"  : "172.172.172.20", 
                    "port"  : 3306, 
                    "db"    : "gscf_user"
                },
                "redis" : { 
                    "host"  : "172.172.172.20", 
                    "port"  : 6379, 
                    "db"    : 0 
                }
            }
        ],
    },
    
    {
        "comment"  :"Analysis: Daily max or min user", 
        "type"     :"APP_RECORD",
        "module"   :"projectXuser", 
        "func"     :"apprec_user_statistics",
        "interval" :1,
        "resources":[
            {
                "mysql" : { 
                    "user"  : "admin", 
                    "passwd": "admin", 
                    "host"  : "192.168.126.8", 
                    "port"  : 3306, 
                    "db"    : "monitor"
                }
            }
        ],
    },
    
    {
        "comment"  :"Collect: Total amount of register and unregister(guest) users", 
        "type"     :"APP_RECORD",
        "module"   :"projectXuser", 
        "func"     :"user_num",
        "interval" :30,
        "resources":[
            {
                "db" : { 
                    "user"  : "gsdba", 
                    "passwd": "yhnmkoert", 
                    "host"  : "172.172.172.20", 
                    "port"  : 3306, 
                    "db"    : "gscf_user"
                }
            }
        ],
    },

    {
        "comment"  :"Analysis: Daily max or min sip register", 
        "type"     :"APP_RECORD",
        "module"   :"projectXuser", 
        "func"     :"daily_sip_register",
        "interval" :86400,
        "resources":[
            {
                "db" : { 
                    "user"  : "admin", 
                    "passwd": "admin", 
                    "host"  : "192.168.126.8", 
                    "port"  : 3306, 
                    "db"    : "monitor"
                }
            }
        ],
    },
  
    # Conference #
    {
        "comment"  :"Collect: Total amount of conference", 
        "type"     :"APP_RECORD",
        "module"   :"projectXconference", 
        "func"     :"conf_num",
        "interval" :30,
        "resources":[
            {
                "db" : { 
                    "user"  : "gsdba", 
                    "passwd": "yhnmkoert", 
                    "host"  : "172.172.172.20", 
                    "port"  : 3306, 
                    "db"    : "gscf_conf"
                }
            }
        ],
    },
    
    {
        "comment"  :"Collect: Number of daily conference",
        "type"     :"APP_RECORD",
        "module"   :"projectXconference", 
        "func"     :"conf_daliy_num",
        "interval" :86400,
        "resources":[
            {
                "db" : { 
                    "user"  : "gsdba", 
                    "passwd": "yhnmkoert", 
                    "host"  : "172.172.172.20", 
                    "port"  : 3306, 
                    "db"    : "gscf_conf"
                }
            }
        ],
    },


    # Files #
    {
        "comment"  :"Collect: Number of daily created files",
        "type"     :"APP_RECORD",
        "module"   :"projectXfile", 
        "func"     :"conf_file_daily_num",
        "interval" :86400,
        "resources":[
                {
                    "db" : { 
                        "user"  : "gsdba", 
                        "passwd": "yhnmkoert", 
                        "host"  : "172.172.172.20", 
                        "port"  : 3306, 
                        "db"    : "gscf_file"
                    }
                }
            ], 
    },

]
            
