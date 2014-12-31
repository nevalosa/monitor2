<?php
/**
 * 
 * 会员查询：会员信息，出席，缴费，演讲
 * @author zhangzr1026
 *
 */
class AboutAction extends Action
{
	public function index(){
		$this->display();
   	}
	
	public function sendMail(){
		
	}
   	
	public function mail() {
		#@date_default_timezone_set('Asia/Shanghai');
		vendor('Smtp.email');
	
		$smtpserver = "mail.wasu.com.cn";//SMTP服务器
		$smtpserverport =25;//SMTP服务器端口
		$smtpusermail = "vip_wasu@wasu.com.cn";//SMTP服务器的用户邮箱
		$smtpemailto ="zhangzr@wasu.com.cn";//发送给谁
		$smtpemail=explode("@",$smtpemailto);


		$mailsubject="TMC Summery中文";
		$mailbody =  $this->fetch();
		//邮件内容
		
		$smtpuser = "vip_wasu@wasu.com.cn";//SMTP服务器的用户帐号
		$smtppass = "wasu1800";//SMTP服务器的用户密码
		$mailtype = "HTML";//邮件格式（HTML/TXT）,TXT为文本邮件
		$smtp = new smtp($smtpserver,$smtpserverport,true,$smtpuser,$smtppass);//这里面的一个true是表示使用身份验证,否则不使用身份验证.
		$smtp->debug = FALSE;//是否显示发送的调试信息
		$mailmsg=$smtp->sendmail($smtpemailto, $smtpusermail, $mailsubject, $mailbody, $mailtype);
		if($mailmsg==true){
			echo "发送到".$smtpemailto."成功<br>";
		}else{
			echo "发送到".$smtpemailto." 失败<br>";
		}

#输出结果
	}
	
	public function mail2() {
		#@date_default_timezone_set('Asia/Shanghai');
		vendor('Smtp.email');
	
		$smtpserver 	= "smtp.163.com";//SMTP服务器
		$smtpserverport = 25;//SMTP服务器端口
		$smtpusermail 	= "zhangzr1026@163.com";//SMTP服务器的用户邮箱
		$smtpemailto 	= "zhangzr@wasu.com.cn";//发送给谁
		$smtpemail	= explode("@",$smtpemailto);
		$cc 	= "zhangzr1026@163.com, zhangzr1026@gmail.com";

		$mailsubject="TMC Summery中文173";
		$mailbody =  $this->fetch('mail');
		//邮件内容
		
		$smtpuser = "zhangzr1026@163.com";//SMTP服务器的用户帐号
		$smtppass = "lonelyisnotalone";//SMTP服务器的用户密码
		$mailtype = "HTML";//邮件格式（HTML/TXT）,TXT为文本邮件
		$smtp = new smtp($smtpserver,$smtpserverport,true,$smtpuser,$smtppass);//这里面的一个true是表示使用身份验证,否则不使用身份验证.
		$smtp->debug = FALSE;//是否显示发送的调试信息
		$mailmsg=$smtp->sendmail($smtpemailto, $smtpusermail, $mailsubject, $mailbody, $mailtype, $cc, $bcc);
		dump($mailmsg);
//		if($mailmsg==true){
//			echo "发送到".$smtpemailto."成功<br>";
//		}else{
//			echo "发送到".$smtpemailto." 失败<br>";
//		}

#输出结果
	}
}

?>