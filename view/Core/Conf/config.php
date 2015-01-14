<?php
return array(
    /* System Define Variables !!!!*/
	//'Config Key'=>'Config Value'
	
	/* DataBase */
	'DB_TYPE' 				=> 'mysql' , 
	'DB_HOST' 				=> '192.168.126.8' , 
	'DB_USER' 				=> 'admin' , 
	'DB_PWD' 				=> 'admin' , 
	'DB_PORT' 				=> '3306' , 
	'DB_NAME' 				=> 'monitor',
	'DB_PREFIX' 			=> '',
		
	/* Cache */
	'TMPL_CACHE_ON' 		=> FALSE,
        
    
    
    /* User Define Variables !!!!*/
    /* Chart Data Type */
    '_RECORDDATATYPE' => array(
        'normal'    => 0 ,
        'hour' 	    => 1 ,
        'day' 		=> 2 ,
        'week' 		=> 3 ,
        'month' 	=> 4 ,
        'season' 	=> 5 ,
        'year' 		=> 6 ,
     )
);
?>