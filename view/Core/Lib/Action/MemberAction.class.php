<?php
/**
 * 
 * 会员查询：会员信息，出席，缴费，演讲
 * @author zhangzr1026
 *
 */
class MemberAction extends CommonAction
{
	public function index(){
//		$condition = array(
//			'ismember' => 1 ,
//		);
		$condition = $this->getMemberCondition($_REQUEST['ismember']);
//		if(isset($_REQUEST['ismember'])){
//			$condition['ismember'] = $_REQUEST['ismember'];
//		}
		$lastmeeting = M('meeting')->field('lastmeeting')->limit(1)->order('mid DESC')->find();
		$this->assign('lastmeeting',$lastmeeting ? $lastmeeting['lastmeeting']:0);
		$this->assign('member',M('member')->where($condition)->order('lastname DESC')->select());
        $this->display();
	}
	
	public function profile(){
		$uid = $_REQUEST['uid'];
		if(!isset($uid)){
			$this->error("uid required");
			die();
		}
		$condition = array(
			'id' => $uid,
		);
		$profile = M('member')->where($condition)->find();
		$this->assign('profile',$profile);
		$this->display();
	}
	
	public function add(){
		$this->display();
	}
	
	public function adding(){
		$data = array(
			'lastname'=>$_REQUEST['lastname'],
			'firstname'=>$_REQUEST['firstname'],
			'cnname'=>$_REQUEST['cnname'],
			'sponsor'=>$_REQUEST['sponsor'],
			'email'=>$_REQUEST['email'],
			'mobile'=>$_REQUEST['mobile'],
			'phone'=>$_REQUEST['phone'],
			'qq'=>$_REQUEST['qq'],
			'level'=>$_REQUEST['level'],
			't_member'=>$_REQUEST['t_member'],
			'ismember'=>$_REQUEST['ismember'],
		);
		$profile = M('member')->data($data)->add();
		if($profile>0){
			$this->assign("jumpUrl","__APP__/Member/edit/uid/$profile");
			$this->success("Add Succeed");
		}
		else{
			$this->error("Add Failed");
		}
	}
	
	public function edit(){
		$uid = $_REQUEST['uid'];
		if(!isset($uid)){
			$this->error("uid required");
			die();
		}
		$condition = array(
			'id' => $uid,
		);
		$profile = M('member')->where($condition)->find();
		$this->assign('profile',$profile);
		$this->display();
	}
	
	public function editing(){
		$uid = $_REQUEST['uid'];
		if(!isset($uid)){
			$this->error("uid required");
			die();
		}
		$condition = array(
			'id' => $uid,
		);
		$data = array(
			'lastname'=>$_REQUEST['lastname'],
			'firstname'=>$_REQUEST['firstname'],
			'cnname'=>$_REQUEST['cnname'],
			'sponsor'=>$_REQUEST['sponsor'],
			'email'=>$_REQUEST['email'],
			'mobile'=>$_REQUEST['mobile'],
			'phone'=>$_REQUEST['phone'],
			'qq'=>$_REQUEST['qq'],
			'level'=>$_REQUEST['level'],
			't_member'=>$_REQUEST['t_member'],
			'ismember'=>$_REQUEST['ismember'],
		);
		$profile = M('member')->data($data)->where($condition)->save();
		if($profile){
			$this->assign("jumpUrl","__APP__/Member/edit/uid/$uid");
			$this->success("Edit Succeed");
		}
		else{
			$this->error("Edit Failed");
		}
	}
	
	public function delete(){
		$uid = $_REQUEST['uid'];
		if(!isset($uid)){
			$this->error("uid required");
			die();
		}
		$condition = array(
			'id' => $uid,
		);
		$profile = M('member')->where($condition)->delete();
		if($profile){
			$this->assign("jumpUrl","__APP__/Member/index/");
			$this->success("Delete Succeed");
		}
		else{
			$this->error("Edit Failed");
		}
	}
	
	/**
	 * 成员类型转换 -> 数据库搜索condition
	 * 成员类型{1,Member},{2,Guest},{3,Officer},{4,Friend Tmc}
	 */ 
	function getMemberCondition($type){
		switch ($type) {
			case 0:
				$condition['ismember'] = array('neq',0);
				break;
		    case 1:
		        $condition['ismember'] = array(array('eq',1),array('eq',3),'or');
		        break;
		    case 2:
		        $condition['ismember'] = array(array('eq',2),array('eq',4),'or');
		        break;
		    case 3:
		        $condition['ismember'] = $type;
		        break;
		    default:
	        	$condition['ismember'] = array('neq',0);
		}
		return $condition;
	}
}

?>