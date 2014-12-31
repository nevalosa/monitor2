<?php
/**
 * 
 * 记录会议信息：届，出席统计，角色，演讲，费用
 * @author zhangzr1026
 *
 */
class MeetingAction extends Action
{
	public function index(){
		$meeting = $this->getMeeting();
		$this->assign('meeting',$meeting);
		$this->display();
	}

	public function getMeeting($where,$field = '*'){
		$meetings = M('meeting')->field($field)->where($where)->order('lastmeeting DESC')->select();
        return $meetings;
	}
	
	public function profile(){
		$mid = $_REQUEST['mid'];
		if(!isset($mid)){
			$this->error("mid required");
			die();
		}
		$condition = array(
			'mid' => $mid,
		);
		$profile = M('meeting')->where($condition)->find();
		$this->assign('profile',$profile);echo 2;
		$this->display();
	}
	
	public function add(){
		$this->display();
	}
	
	public function adding(){
		$lastmeeting = M('meeting')->field('no,lastmeeting')->order('no DESC')->find();
		if($lastmeeting){
			$data = array(
				'no'			=> intval($lastmeeting['no']) + 1,
				'lastmeeting'	=> strtotime( date('Ymd', intval($lastmeeting['lastmeeting']) + 7*24*3600) ),
			);
		}
		else{
			$data = array(
				'no'			=> 1,
				'lastmeeting'	=> time(),
			);
		}
		$profile = M('meeting')->data($data)->add();
		if($profile>0){
			$this->assign("jumpUrl","__APP__/Meeting/edit/mid/$profile");
			$this->success("Add Succeed");
		}
		else{
			$this->error("Add Failed");
		}
	}
	
	public function edit(){
		$mid = $_REQUEST['mid'];
		if(!isset($mid)){
			$this->error("mid required");
			die();
		}
		$condition = array(
			'mid' => $mid,
		);
		$profile = M('meeting')->where($condition)->find();
		$this->assign('profile',$profile);
		$this->display();
	}
	
	public function editing(){
		$mid = $_REQUEST['mid'];
		if(!isset($mid)){
			$this->error("mid required");
			die();
		}
		$condition = array(
			'mid' => $mid,
		);
		$data = array(
			'no'=>$_REQUEST['no'],
			'lastmeeting'=>strtotime($_REQUEST['lastmeeting']),
			'toastmaster'=>$_REQUEST['toastmaster'],
			'fee_input_member'=>$_REQUEST['fee_input_member'],
			'fee_input_guest'=>$_REQUEST['fee_input_guest'],
			'fee_input_other'=>$_REQUEST['fee_input_other'],
			'fee_output_rent'=>$_REQUEST['fee_output_rent'],
			'fee_output_prize'=>$_REQUEST['fee_output_prize'],
			'fee_output_ohter'=>$_REQUEST['fee_output_ohter'],
		);
		$profile = M('meeting')->data($data)->where($condition)->save();
		if($profile){
			$this->assign("jumpUrl","__APP__/Member/edit/mid/$mid");
			$this->success("Edit Succeed");
		}
		else{
			$this->error("Edit Failed");
		}
	}
	
	public function delete(){
		$mid = $_REQUEST['mid'];
		if(!isset($mid)){
			$this->error("mid required");
			die();
		}
		$condition = array(
			'id' => $mid,
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
	
	public function exportMember(){
		$lastmeeting = $_REQUEST['lastmeeting'];
		if(!isset($lastmeeting)){
			$this->error("meeting required");
			die();
		}
		
		//签到信息
		$present = $this->presentInfo($lastmeeting);
		$this->assign('present',$present);
		
		//会议信息
		$profile = M('meeting')->WHERE(array('lastmeeting'=>$lastmeeting))->find();
		$this->assign('profile',$profile);
		
		$this->display();
	}
	
	public function presentInfo($lastmeeting){
		$sql = "
		SELECT p.*, mem.*
		FROM 
			tms_present AS p
			LEFT JOIN tms_member AS mem ON p.uid = mem.id
		WHERE  
			p.lastpresent = '$lastmeeting'
		ORDER BY 
			ismember, firstname
		";
		return M()->query($sql);
	}
	
	public function editexportMember(){
		$uid = $_REQUEST['uid'];
		$lastpresent = $_REQUEST['lastpresent'];
		if(!isset($uid) || !isset($lastpresent)){
			$this->error("uid or lastpresent required");
			die();
		}
		$sql = "
		SELECT p.*, mem.cnname, meet.no
		FROM 
			tms_present AS p
			LEFT JOIN tms_member AS mem ON p.uid = mem.id
			LEFT JOIN tms_meeting AS meet ON p.lastpresent = meet.lastmeeting
		WHERE  
			p.lastpresent = '$lastpresent' and p.uid = '$uid'
		LIMIT
			1
		";
		$profile = M()->query($sql);
		$this->assign('profile',$profile[0]);
		$this->display();
	}
	
	public function editingexportMember(){
		$uid = $_REQUEST['uid'];
		$lastpresent = $_REQUEST['lastpresent'];
		if(!isset($uid) || !isset($lastpresent)){
			$this->error("uid or lastpresent required");
			die();
		}
		$condition = array(
			'uid' => $uid,
			'lastpresent' => $lastpresent,
		);		
		$data = array(
			'fee'=>$_REQUEST['fee'],
			'remark'=>$_REQUEST['remark'],
		);
		$profile = M('present')->data($data)->where($condition)->save();
		if($profile){
			$this->assign("jumpUrl","__APP__/Meeting/editexportMember/uid/$uid/lastpresent/$lastpresent");
			$this->success("Edit Succeed");
		}
		else{
			$this->error("Edit Failed");
		}
	}
	
	public function sendmail(){
		vendor('Smtp.email');
		
		//获取发件人列表
		$smtpemailto = 'zhangzr@wasu.com.cn';//A('Mail')->getMail(1);
		
		//获取会议信息(内容)
		$lastmeeting = $_REQUEST['lastmeeting'];
		if(!isset($lastmeeting)){
			$this->error("meeting required");
			die();
		}
		$present = $this->presentInfo($lastmeeting);
		$this->assign('present',$present);
		$mailbody = $this->fetch('sendmail1');
		$this->display('sendmail1');
		#die();
		//获取发件主题
		$mailsubject = '西子TMC'. date('Y年m月d日', $lastmeeting) .'会议报告';
		$smtp = new smtp(SMTPSERVER,SMTPSERVERPORT,true,SMTPUSER,SMTPPASS);//这里面的一个true是表示使用身份验证,否则不使用身份验证.
		$mailmsg=$smtp->sendmail($smtpemailto, SMTPUSERMAIL, $mailsubject, $mailbody, 'HTML');
		if($mailmsg==true){
			echo "发送到".$smtpemailto."成功<br>";
		}else{
			echo "发送到".$smtpemailto." 失败<br>";
		}
	}
}

?>