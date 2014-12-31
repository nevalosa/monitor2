<?php
/**
 * 
 * Ajax
 * @author zhangzr1026
 *
 */
class AjaxAction extends Action
{	
	private $status = array(
		'1' => 'success' ,
	);
	
	public function index(){
		echo "aa";
 	}

	public function membersign(){
		$Mm = M('member');
		$Mp = M('present');
		$uid = $_REQUEST["uid"];
		$sign = $_REQUEST["sign"];
		$fee = $_REQUEST["fee"];
		$lastmeeting = isset($_REQUEST["lastmeeting"]) ? $_REQUEST["lastmeeting"] : $this->getToday();
		//检测用户
		$uid = $_REQUEST["uid"];
		if(!$uid > 0){
			die('-1');//缺少ID
		}
		$Rm = $Mm->where("id=".$uid)->find();
		if(empty($Rm)){
			die('-2');//用户不存在
		}
		//检查缴费
		if(empty($fee)){
			if($Rm['ismember'] == 1){
				$fee = 10.00;
			}
			else{
				$fee = 20.00;
			}
		}
		//检测是否已经插入
		$condition = array(
			'uid' => $uid , 
			'lastpresent' => $lastmeeting ,
		);
		$Rp = $Mp->where($condition)->find();
		if(!empty($Rp)){
			die('-3');//签到数据已存在
		}
		//插入数据
		$save = array(
			'uid' => $uid , 
			'lastpresent' => $lastmeeting , 
			'fee' => $fee , 
		);
		$InsertId = $Mp->add($save);
		if(!$InsertId > 0){
			die('-4');//插入失败
		}
		echo 1;//成功
	}
	
	function getToday(){
		$time = date("Y-m-d 00:00:00");
		$unixTimeStamp = strtotime($time);
		return strtotime($time);
	}
	
}

?>