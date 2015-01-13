<?php

class CommonAction extends Action
{
	protected $browser;
	
	protected function _initialize(){
		//检测浏览器
		if(strpos($_SERVER['HTTP_USER_AGENT'],"iPhone")){
			$this->browser = 'iphone';
		}
		else{
			$this->browser = 'other';
		}
		$this->assign('browser',$this->browser);
		
		//Set Side Bar Status
		$this->assign('SideNavStatus',$this->getSideNavStatus());
   }
 
   //Get Side Bar Status
   protected function getSideNavStatus()
   {
       $SideNavStatus = array();
       //$_REQUEST['SideNavStatus'] = "SideNav_Customer,SideNav_Conference";
       $SideNavOn = explode(",",$_REQUEST['SideNavStatus']);
       foreach ($SideNavOn as $val){
           $SideNavStatus[$val] = 'on';
       }
       return $SideNavStatus;
   }
}

?>