<?php

/* CustomerAction */
class CustomerAction extends CommonAction
{
    /**
    +----------------------------------------------------------
    * Default Page
    +----------------------------------------------------------
    */
	public function index()
    {
        $this->display();
    }
    
    public function live()
    {
        // Set Chart
        $this->assign('yAxis_title', 'User Number');
        
        // Draw Temple
        $this->display();
    }
    
    public function statistics()
    {
    
        // Draw Temple
        $this->display();
    }
}
?>