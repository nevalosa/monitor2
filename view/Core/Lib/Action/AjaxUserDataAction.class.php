<?php
class AjaxUserDataAction extends AjaxChartDataAction
{	

    public function RegisteredUser(){
        echo $this->getChartData("AjaxChartData","getUserNum","real_time","register_user");
    }
    
    public function Guest(){
        echo $this->getChartData("AjaxChartData","getUserNum","real_time","guest_user");
    }
    
    public function SipOnlineUser(){
        echo $this->getChartData("AjaxChartData","getUserNum","real_time","sip_online_user");
    }
    
    public function WebOnlineUser(){
        echo $this->getChartData("AjaxChartData","getUserNum","real_time","web_online_user");
    }
    
}
?>
