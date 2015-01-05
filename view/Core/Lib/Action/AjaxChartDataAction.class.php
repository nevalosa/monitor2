<?php
class AjaxChartDataAction extends CommonAction
{	
    //////////////////
    // Host Monitor //
    //////////////////
    public function getChartData($modelName,$modelFunc,$dataName="real_time",$valName="num",$dataZoom=1)
    {
        $LIMITMAX = 0; //Max num of dispkay data

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

        // default 'Normal(0)'
        $type   = empty($_REQUEST['type'])  ? '0'  : $_REQUEST['type'];
        
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
                $chart[] = [$GMT_UNIX_TS*1000, floatval($data["value"])];
            else //with 'h' param, use formatted time
                #$chart[] = $data;
                $chart[] = [$data["date"], floatval($data["value"])];
        }
        return json_encode($chart);

    }
    
    public function RegisteredUser(){
        echo $this->getChartData("AjaxChartData","getUserNum","real_time","register_user");
    }
    
    public function Guest(){
        echo $this->getChartData("AjaxChartData","getUserNum","real_time","guest_user");
    }
    
    public function SipOnlineUser(){
        echo $this->getChartData("AjaxChartData","getSipUserNum","real_time","num");
    }
    
    public function WebOnlineUser(){
        echo $this->getChartData("AjaxChartData","getSipUserNum","real_time","num");
    }
    
	public function index_bak(){

		//实例化Monitor Model，具体方法请看 MonitorModel.class.php
		$model = D('Monitor');

		//获取所有服务器列表信息；
		$result = $model->getAllServerInfo();
        for($i=0;$i<count($result);$i++)
        {
            if($result[$i]["status"] == "offline" )
                continue;
            $result[$i]["last_hours"]=sprintf("%.01f", $result[$i]["last_hours"]/3600 );
            $host = $model->getHost($result[$i]["host_id"]);
            $result[$i]["load_average"] = $host["load_average"];

            $fsList = $model->getFsList($result[$i]["host_id"]);
            for($j=0;$j<count($fsList);$j++)
            {
                $result[$i]["total_size"] = (int)$result[$i]["total_size"] + (int)$fsList[$j]["total_size"];
                $result[$i]["used_size"] = (int)$result[$i]["used_size"] + (int)$fsList[$j]["used_size"];
            }
            $result[$i]["space_used_percent"] = sprintf('%.0f',$result[$i]["used_size"] / $result[$i]["total_size"] * 100);
            $result[$i]["h_total_size"]   = sprintf('%.0f',$result[$i]["total_size"]/1024);
            $result[$i]["h_used_size"]    = sprintf('%.0f',$result[$i]["used_size"]/1024);

        }
		$this->assign("datalist",$result);
		$this->display();
	}

	public function serverInfo(){
		
		$host_id	= $_REQUEST['id']; // 获得传递过来的参数

		//实例化Monitor Model，具体方法请看 MonitorModel.class.php
		$model		= D('Monitor');

        //Host Info
        $host = $model->getHost($host_id);

        $this->assign("host",$host);

        //Network Card List
        $nclist = $model->getNetworkList($host_id); 

        $this->assign("nclistsize",count($nclist));
        $this->assign("nclist", $nclist);

        //Disk List
        $disklist = $model->getDiskList($host_id); 

        for($i=0;$i<count($disklist);$i++)
        {
            $disklist[$i]['h_disk_capacity'] = $disklist[$i]['disk_capacity']>1024 ? intval($disklist[$i]['disk_capacity']/1024) . "G" : intval($disklist[$i]['disk_capacity']) . "M";
        }

        $this->assign("disklistsize",count($disklist));
        $this->assign("disklist", $disklist);

		//FileSystem List
		$hlist = $model -> getDetailDiskInfo($host_id);

        for($i=0;$i<count($hlist);$i++)
        {
            $hlist[$i]['h_total_size'] = $hlist[$i]['total_size']>1024 ? intval($hlist[$i]['total_size']/1024) . "G" : intval($hlist[$i]['total_size']) . "M";
            $hlist[$i]['h_used_size'] = $hlist[$i]['used_size']>1024 ? intval($hlist[$i]['used_size']/1024) . "G" : intval($hlist[$i]['used_size']) . "M"; 
            $hlist[$i]['h_avail'] = $hlist[$i]['total_size'] - $hlist[$i]['used_size'];
            $hlist[$i]['h_avail'] = $hlist[$i]['h_avail']>1024 ? intval($hlist[$i]['h_avail']/1024) . "G" : intval($hlist[$i]['h_avail']) . "M"; 
        }

		$this->assign("fslist",$hlist);
	    $this->assign("fslistsize",count($hlist));



	    $this->display('serverInfo');
	}

	public function diskInfo(){
		
		$diskid	= $_REQUEST['id']; // 获得传递过来的参数
		$model = D('Monitor');
        $disk = $model->getDisk($diskid);
        $disk['h_disk_capacity'] = $disk['disk_capacity']>1024 ? intval($disk['disk_capacity']/1024) . " G" : intval($disk['disk_capacity']) . " M";
        $this->assign("disk",$disk);
	    $this->display('diskInfo');
	}

	public function ncInfo(){
		
		$ncid	= $_REQUEST['id']; // 获得传递过来的参数
		$model = D('Monitor');
        $nc = $model->getNc($ncid);

        $this->assign("nc",$nc);
	    $this->display('ncInfo');
	}

    public function chartcpuload(){
        echo $this->chart("Monitor","getCPUHistory","real_time","load_average");
    }

    public function chartcpuiowait(){
        echo $this->chart("Monitor","getCPUHistory","real_time","cpu_iowait");
    }

    public function chartcpusys(){
        echo $this->chart("Monitor","getCPUHistory","real_time","cpu_sys");
    }

    public function chartcpuuser(){
        echo $this->chart("Monitor","getCPUHistory","real_time","cpu_user");
    }

    public function chartcpuidle(){
        echo $this->chart("Monitor","getCPUHistory","real_time","cpu_idle");
    }

    public function chartmemused(){
        echo $this->chart("Monitor","getCPUHistory","real_time","mem_used");
    }

    public function chartmemfree(){
        echo $this->chart("Monitor","getCPUHistory","real_time","mem_free");
    }

    public function chartmembuffers(){
        echo $this->chart("Monitor","getCPUHistory","real_time","mem_buffers");
    }

    public function chartmemcached(){
        echo $this->chart("Monitor","getCPUHistory","real_time","mem_cached");
    }

    public function chartswapused(){
        echo $this->chart("Monitor","getCPUHistory","real_time","swap_used");
    }

    public function chartswapfree(){
        echo $this->chart("Monitor","getCPUHistory","real_time","swap_free");
    }

    public function chartdisktps(){
        echo $this->chart("Monitor","getDiskHistory","real_time","tps");
    }

    public function chartdiskrsec(){
        echo $this->chart("Monitor","getDiskHistory","real_time","rsec",0.5);
    }

    public function chartdiskwsec(){
        echo $this->chart("Monitor","getDiskHistory","real_time","wsec",0.5);
    }

    public function chartdiskavgrqsz(){
        echo $this->chart("Monitor","getDiskHistory","real_time","avgrq_sz");
    }

    public function chartdiskavgqusz(){
        echo $this->chart("Monitor","getDiskHistory","real_time","avgqu_sz");
    }

    public function chartdiskawait(){
        echo $this->chart("Monitor","getDiskHistory","real_time","await");
    }

    public function chartdisksvctm(){
        echo $this->chart("Monitor","getDiskHistory","real_time","svctm");
    }

    public function chartdiskutil(){
        echo $this->chart("Monitor","getDiskHistory","real_time","util");
    }

    public function chartncrxpck(){
        echo $this->chart("Monitor","getNcHistory","real_time","rxpck");
    }

    public function chartnctxpck(){
        echo $this->chart("Monitor","getNcHistory","real_time","txpck");
    }

    public function chartncrxkb(){
        echo $this->chart("Monitor","getNcHistory","real_time","rxkb");
    }

    public function chartnctxkb(){
        echo $this->chart("Monitor","getNcHistory","real_time","txkb");
    }

    public function chartv1interfaceaccess(){
        echo $this->chart("Monitor","getV1InterfaceHistory","real_time","total_access");
    }

    public function chartv1interfacesuccessrate(){
        echo $this->chart("Monitor","getV1InterfaceHistory","real_time","success_rate");
    }

    public function chartv1interfacetimeelapsed(){
        echo $this->chart("Monitor","getV1InterfaceHistory","real_time","time_elapsed");
    }
    
    public function chart($modelName,$modelFunc,$dataName,$valName,$dataZoom=1)
    {
        $LIMITMAX = 30; //Max num of dispkay data

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

	$id = empty($_REQUEST['id'])? 1         : $_REQUEST['id']; 
        $type   = empty($_REQUEST['type'])  ? 'normal'  : $_REQUEST['type'];

        //Model
        $model  = D($modelName);
	$result = $model->$modelFunc($id,$type,$start,$end);
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
            $chart[] = $data;
        }
        return json_encode($chart);

    }

    ///////////////////
    // MySQL Monitor //
    ///////////////////
    public function zmysqlindex()
    {
        $this->display();
    }

    public function zmysqlinfo()
    {
        $this->display();
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
