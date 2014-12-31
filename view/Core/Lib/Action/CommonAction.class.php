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
   }

}

?>