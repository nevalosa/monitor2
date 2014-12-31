<?php
/**
 * 
 * 会员查询：会员信息，出席，缴费，演讲
 * @author zhangzr1026
 *
 */
class MailAction extends CommonAction
{
	//显示邮件列表的分隔符
	private $separator = ',';
	//邮件显示方式
	private $displayMethod = 'list';
	
	public function index(){
		$ismember = $_REQUEST['ismember'];
		$mailList = $this->getMail($ismember,'email,lastname,firstname,cnname');
		$this->assign('mailList',$mailList);
		$this->display();
	}
	
	/**
	 * 
	 * 获取邮件列表，返回结果集
	 * @param int $ismember 成员类型{1,Member},{2,Guest},{3,Officer},{4,Friend Tmc}
	 * @param string $field 数据列名列表，mail为必须,比如'email,lastname,firstname,cnname'
	 */
	public function getMail($ismember=1,$field='email'){
		if(isset($ismember)){
			$where = array('ismember'=>$ismember);
		}
		$Mails = M('member')->field($field)->where($where)->order('lastname DESC')->select();
        return $Mails;
	}
	
	public function excelDownload($params) {
		
		$params = M('member')->select();
		
		Vendor ( 'office.PHPXml.excelxml' );
		! defined ( 'UPLOAD_PATH' ) && define ( 'UPLOAD_PATH', './UploadFile/' );
		// source file
		$input = THINK_PATH . '/Vendor/office/PHPXml/input.xml';
		// output file
		$output = UPLOAD_PATH . '/xls_temp/output.xml';
		$filepath = UPLOAD_PATH . '/xls_temp/output.xls';
		
		// create ExcelXML object
		$xml = new ExcelXML();
		if (!$xml->read($input))
		{
			return FALSE;
		}
		else
		{
			// activate a worksheet
			$xml->setActiveWorksheetByIndex(0);
			// get cell value
			#echo $xml->getCellValue("A1") . "<br>";
			// set cell value
			$xml->setCellValue('A1', 'First Name');
			$xml->setCellValue('B1', 'Last Name');
			$xml->setCellValue('C1', '姓名');
			$xml->setCellValue('D1', '介绍人');
			$xml->setCellValue('E1', 'Email');
			$xml->setCellValue('F1', 'Mobile');
			$xml->setCellValue('G1', '是否接收预告');
			$xml->setCellValue('H1', '备注');
			        
			$i= 1;
			while($row = $params[$i-1]){
				$i++;
				$xml->setCellValue('A'.$i, $row['lastname']);
			    $xml->setCellValue('B'.$i, $row['firstname']);
			    $xml->setCellValue('C'.$i, $row['cnname']);
			    $xml->setCellValue('D'.$i, $row['sponsor']);
			    $xml->setCellValue('E'.$i, $row['email']);
			    $xml->setCellValue('F'.$i, $row['mobile']);
			    $xml->setCellValue('G'.$i, '1');
			    $xml->setCellValue('H'.$i, '20');
			}
			// save modified file to output file
//			if (!$xml->save($output))
//				echo "Failed to save file<br>";
//			else
//				echo "Succeed to save file<br>";
			/** uncomment following codes, so client can download Excel (*.xls) file **/
			//$xml->save($output);
			$xml->save($output, true, $filepath);
		}
		
		#echo '<a href="/UploadFile/xls_temp/output.xlsx?date=' . time () . '">download</a>';
		#return $filepath;
	}
}

?>