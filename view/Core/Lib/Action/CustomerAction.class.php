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
        $this->display();
    }
}
?>