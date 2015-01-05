<?php
class AjaxChartDataModel extends Model {
	
	protected $_dbname	= 'monitor';
	protected $_table;
	protected $_connected;
	protected $_port	= '3306';
 
	public function __construct(){

		//数据库连接操作，实例化$_connected;
		$conn = 'mysql://'.C('DB_USER').':'.C('DB_PWD').'@'.C('DB_HOST').':'.$this->_port.'/'.$this->_dbname;
 		$this->_connected = M('','AdvModel');
 		$this->_connected->addConnect($conn,2);
 		$this->_connected->switchConnect(2);
	}
	
	public function getUserNum($type, $start, $end, $cond){
	    $where = "real_time>'$start' AND real_time<'$end' AND type='$type' ";
	
	    $result = M('apprec_user_num')
	    ->where($where)
	    ->order("real_time ASC")
	    ->select();
	    return $result;
	}
	
	public function getSipUserNum($type, $start, $end, $cond){
	    $where = "real_time>'$start' AND real_time<'$end' AND type='$type' ";
	    
	    $result = M('apprec_user_sip_num')
	    ->where($where)
	    ->order("real_time ASC")
	    ->select();
	    return $result;
	}	

	public function getHost($host_id){
		$result = $this->_connected->table('info_host')->where("host_id=$host_id")
                    ->find();
	        $history = $this->_connected->table('info_host_history')
                ->where("host_id=$host_id and type='normal'")
                ->order("real_time desc")
                ->find();

        foreach($history as $key=>$val)
        {
            if(!$result[$key])
                $result[$key] = $history[$key];
        }
		return $result;
	}

	public function getDisk($disk_id){
		$result = $this->_connected->table('info_disk')->where("disk_id=$disk_id")
                    ->find();
        return $result;
	}

	public function getNc($nc_id){
		$result = $this->_connected->table('info_networkcard')->where("nc_id=$nc_id")
                    ->find();
        return $result;
	}

	public function getAllServerInfo(){

		//获取所有服务器列表信息,若需更多信息，请修改。
		$result = $this->_connected->table('info_host')
                    ->select();
		return $result;
	}

	public function getDetailDiskInfo($host_id=''){
		
		if(!intval($host_id)){
			return null;
		}

		//根据服务器编号，获取器磁盘信息，若需更多信息，请修改。
		$result	= $this->_connected->table('info_filesystem')
								 ->where('host_id='.$host_id)
								 ->select();
		return $result;
	}

	public function getCPUHistory($hostid,$type,$start,$end){
		$where = "real_time>'$start' AND real_time<'$end' AND host_id=$hostid AND type='$type'";

		$result = $this->_connected->table('info_host_history')
									->where($where)
									->select();
		return $result;
	}

	public function getDiskHistory($diskid,$type,$start,$end){
		$where = "real_time>'$start' AND real_time<'$end' AND disk_id=$diskid AND type='$type'";

		$result = $this->_connected->table('info_disk_history')
									->where($where)
									->select();
		return $result;
	}

	public function getNcHistory($ncid,$type,$start,$end){
		$where = "real_time>'$start' AND real_time<'$end' AND nc_id=$ncid AND type='$type'";

		$result = $this->_connected->table('info_networkcard_history')
									->where($where)
									->select();
		return $result;
	}

	public function getV1InterfaceHistory($interfaceid,$type,$start,$end){
		$where = "real_time>'$start' AND real_time<'$end' AND interface_id=$interfaceid AND type='$type'";

		$result = $this->_connected->table('v1_interface_history')
									->where($where)
									->select();
		return $result;
	}

	public function getMemoryInfo($datetime,$hostid,$type,$limit){
		if(!$datetime || !$hostid || !$type){
			return null;
		}

		$where = array(
			'host_id'	=> 	$hostid,
			'type'		=>	$type,
			'real_time'	=>	array('elt',$datetime)
		);

		$result = $this->_connected->table('info_host_history')
									->where($where)
									->field('real_time,memory_used,memory_free,memory_buffers,memory_cached')
									->limit($limit)
									->select();
		return $result;
	
	}

	public function getSwapInfo($datetime,$hostid,$type,$limit){
		if(!$datetime || !$hostid || !$type){
			return null;
		}

		$where = array(
			'host_id'	=> 	$hostid,
			'type'		=>	$type,
			'real_time'	=>	array('elt',$datetime)
		);

		$result = $this->_connected->table('info_host_history')
									->where($where)
									->field('swap_used,swap_free')
									->limit($limit)
									->select();
		return $result;
	}

	public function getNetworkList($host_id){
		
		if(!intval($host_id)){
			return null;
		}

		$result	= $this->_connected->table('info_networkcard')
								 ->where('host_id='.$host_id)
								 ->select();
		return $result;
	}

	public function getDiskList($host_id){
		
		if(!intval($host_id)){
			return null;
		}

		$result	= $this->_connected->table('info_disk')
								 ->where('host_id='.$host_id)
								 ->select();
		return $result;
	}

	public function getFsList($host_id){
		
		if(!intval($host_id)){
			return null;
		}

		$result	= $this->_connected->table('info_filesystem')
								 ->where('host_id='.$host_id)
								 ->select();
		return $result;
	}

	public function getAppList(){
		$result = $this->_connected->table('app_common')->order('app_name')
                    ->select();
		return $result;
	}

	public function getAppTypeList(){
		$result = $this->_connected->table('app_type')->order('type_name')
                    ->select();
		return $result;
	}

}
?>
