<?php 
/**
 * 今天的时间
 */
function getToday(){
	$time = date("Y-m-d 00:00:00");
	return $time;#strtotime("20121221");
}

/**
 * 星期
 */ 
function getWeekName($d){
	$weekdArray = array(
						0 => "日", 
						1 => "一", 
						2 => "二", 
						3 => "三", 
						4 => "四", 
						5 => "五", 
						6 => "六"
					);
	return $weekdArray[$d];
}

/**
 * 成员类型转换 -> 数据库搜索condition
 * 成员类型{1,Member},{2,Guest},{3,Officer},{4,Friend Tmc}
 */ 
function getMemberCondition($type){
//	$MType = array(
//		'All' => 0,
//		'Member' => 1,
//		'Guest' => 2,
//		'Officer' => 3,
//		'Friend' => 4,
//	);
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

?>