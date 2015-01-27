<?php
class AjaxChartDataAction extends CommonAction
{	
    //////////////////
    // Host Monitor //
    //////////////////
    public function getChartData($modelName,$modelFunc,$dataName="real_time",$valName="num",$dataZoom=1)
    {
        $LIMITMAX = 100; //Max num of dispkay data

        //$REQUEST
        if(empty($_REQUEST['start']) || empty($_REQUEST['end']))
        {
            $start  = date("Y-m-d 00:00:00");
            $end    = date("Y-m-d 23:59:59");
        }
        else{
            $start  = $_REQUEST['start'];
            $end    = $_REQUEST['end'];
        }

        // default 'Normal(0)', reference to "config.php's _RECORDDATATYPE" which is "C('_RECORDDATATYPE')"
        $_RECDT =  C('_RECORDDATATYPE');
        $type   = empty($_REQUEST['type'])  ? '0'  : $_RECDT[$_REQUEST['type']];
                
        // conditions
        $cond = empty($_REQUEST['cond'])    ? ''   : $_REQUEST['cond'];

        //Model
        $model  = D($modelName);
	    $result = $model->$modelFunc($type, $start, $end, $cond);
        $chart = array();
        
        //Inteval
        $inteval = (int)(count($result)/$LIMITMAX);
        
        //
        for($i=0;$i<count($result);$i++){
            if( $LIMITMAX> 0 && $i>0 && $i%$inteval !=0 )
                continue;
            $data = array();
            $data["date"]   = $result[$i][$dataName] ; 
            $data["value"]  = $result[$i][$valName]; 

            if($dataZoom > 1)
                $data["value"] = sprintf("%.2f" , $data["value"] / $dataZoom);
            
            $DATEFORMAT="%Y-%m-%d %H:%M:%S";
            
            $UNIX_TS = strtotime($data["date"]);
            $MAP_T = getdate($UNIX_TS);
            $GMT_UNIX_TS = gmmktime($MAP_T['hours'],$MAP_T['minutes'],$MAP_T['seconds'],$MAP_T['mon'],$MAP_T['mday'],$MAP_T['year']);
            
            if(empty($_REQUEST['h'])) // UTC Timestamp(microsecond)
                $chart[] = array($GMT_UNIX_TS*1000, floatval($data["value"]));
            else //with 'h' param, use formatted time
                #$chart[] = $data;
                $chart[] = array($data["date"], floatval($data["value"]));
        }
        return json_encode($chart);

    }
    
    

    ///
    public function appindex()
    {
 		$model = D('Monitor');

		$result = $model->getAppList();
        $this->assign("datalist",$result);

        $appTypeList = $model->getAppTypeList();
        $this->assign("apptypelist",$appTypeList);

        $this->display();
    }


   
}
?>
