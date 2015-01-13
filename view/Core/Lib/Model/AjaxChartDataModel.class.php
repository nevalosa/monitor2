<?php
class AjaxChartDataModel extends Model {
	
	protected $_dbname	= 'monitor';
	protected $_table;
	protected $_connected;
	protected $_port = '3306';
	protected $_limit = 0;
 
	public function __construct(){

		//数据库连接操作，实例化$_connected;
		$conn = 'mysql://'.C('DB_USER').':'.C('DB_PWD').'@'.C('DB_HOST').':'.$this->_port.'/'.$this->_dbname;
 		$this->_connected = M('','AdvModel');
 		$this->_connected->addConnect($conn,2);
 		$this->_connected->switchConnect(2);
	}
	
	public function getUserNum($type, $start, $end, $cond){
	    $where = "real_time>'$start' AND real_time<'$end' AND type='$type' ";
	    $result = M('apprec_user')
	    ->where($where)
	    ->order("real_time ASC")
	    ->limit($this->_limit)
	    ->select();
	    return $result;
	}

}
?>
