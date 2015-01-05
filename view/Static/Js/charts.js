//-------------------prepare data----------------------//
$(document).ready(function() {
	// Set Time
	calculateDate();
	
	// Bind Click Event
	$("#ajaxDistrict :radio").click(function(){
		rewriteChart()
	});
	$("#ajaxHosts :checkbox").click(function(){
		rewriteChart()
	});
	$("#ajaxOptions :checkbox").click(function(){
		rewriteChart()
	});
	
	// Write Init Chart
	rewriteChart();
});

// Global Chart Data Cache
var ChartDataCache={};
/*
ChartDataCache['172.172.172.18_day_siponlineuser']={
        name: 'data1',
        data: [
			[Date.UTC(2015,  1, 4,10,0,0), 1   ],
			[Date.UTC(2015,  1, 4,11,0,0), 10   ],
			[Date.UTC(2015,  1, 4,12,0,0), 100  ],
			[Date.UTC(2015,  1, 4,13,0,0), 1000   ],
        ]
	};
*/
// Get Chart Params for Ajax
function getChartParams(){
	params = {"type":"normal",
			"start":"2014-01-05 00:00:00",
			"end":"2015-01-05 00:00:00"
	}
	return params
}

//ajax rewrite chart
function rewriteChart(){
	//$('#debugframe').html("a")
	
	//$('#debugframe').html(JSON.stringify(ChartDataCache))
	var seriesVal=[];
	
	/*
	$("#ajaxHosts :checkbox").each(function(hostIndex,hostElement ){
		if(hostElement.checked == true){
			$("#ajaxOptions :checkbox").each(function(optIndex,optElement ){
				if(optElement.checked == true){
					//Get Data Cache's Key
					combineKey = hostElement.value+'_day_'+optElement.value;
					//if  Data Cache not exists, get value from ajax
					if(typeof(ChartDataCache[combineKey])=="undefined"){
						ajaxData=requestAjax('/index.php/'+ajaxModuleName+'/'+optElement.value,
							getChartParams(), dataFormat);
						ChartDataCache[combineKey]={
						        name: hostElement.value+'\'s '+optElement.value,
						        data: ajaxData
							};
						seriesVal.push(ChartDataCache[combineKey]);
					}
					//Data Cache exists, add it to the 'Chart Series'
					else{ 
						seriesVal.push(ChartDataCache[combineKey]);
					}
				}
			});
		}			
	    	
	});
	*/
	
	$("#ajaxOptions :checkbox").each(function(optIndex,optElement ){
		if(optElement.checked == true){
			
			if( $("#ajaxHost :checkbox").length ==0 )
			{
				//Get Data Cache's Key
				combineKey = optElement.value + "_day_";
				//if  Data Cache not exists, get value from ajax
				if(typeof(ChartDataCache[combineKey])=="undefined"){
					ajaxData=requestAjax('/index.php/'+ajaxModuleName+'/'+optElement.value,
						getChartParams(), dataFormat);
					ChartDataCache[combineKey]={
					        name: optElement.value,
					        data: ajaxData
						};
					seriesVal.push(ChartDataCache[combineKey]);
				}
				//Data Cache exists, add it to the 'Chart Series'
				else{ 
					seriesVal.push(ChartDataCache[combineKey]);
				}
			}
			else
			{
				$("#ajaxHosts :checkbox").each(function(hostIndex,hostElement ){
					if(hostElement.checked == true){
						//Get Data Cache's Key
						combineKey = hostElement.value+'_day_'+optElement.value;
						//if  Data Cache not exists, get value from ajax
						if(typeof(ChartDataCache[combineKey])=="undefined"){
							ajaxData=requestAjax('/index.php/'+ajaxModuleName+'/'+optElement.value,
								getChartParams(), dataFormat);
							ChartDataCache[combineKey]={
							        name: hostElement.value+'\'s '+optElement.value,
							        data: ajaxData
								};
							seriesVal.push(ChartDataCache[combineKey]);
						}
						//Data Cache exists, add it to the 'Chart Series'
						else{ 
							seriesVal.push(ChartDataCache[combineKey]);
						}
					}			
				    	
				});
			}
		}
	});
	
	
	
	
	var title, xAxis, yAxis, tooltip, url;
	
	var chartType='spline'
	
	
	$('#realTimeChart').highcharts({
		// Default False
    	credits:{
   	     enabled:false
	   	},
	   	legend:{
	  	     enabled:false
	   	},
	   	
	   	// Optional
    	chart: {
            type: chartType                         //指定图表的类型，默认是折线图（line）
        },
        title: {
            text: 'My first Highcharts chart'      //指定图表标题
        },
        xAxis: { 
        	type: 'datetime',
        	dateTimeLabelFormats:{
        		millisecond: '%H:%M:%S.%L',
        		second: '%H:%M:%S',
        		minute: '%H:%M',
        		hour: '%H:%M',
        		day: '%y/%m/%d',
        		week: '%y/%m/%d',
        		month: '%b \'%y',
        		year: '%Y'
        	},
        },
        title: {
            text: 'Date'
        },
        yAxis: {
            title: {
                text: 'something'                  //指定y轴的标题
            },
            min: 0
        },
        series: seriesVal
    });
	
	return true;
}

//ajax request for data
function requestAjax(url, param, next){
	var result;
	$.ajax({
		type: "get",
		url : url,
		data : param,
		async: false,
		dataType : "json",
		success : function(data){
			//result = next(data);
			result = data;
		}
	});
	return result;
}

//calculate time range
function calculateDate(){
	var date_today = new Date();
	var date_weekago =  new Date(date_today.getTime() - 7*24*60*60*1000);
	var date_monthago =  new Date(date_today.getTime() - 30*24*60*60*1000);
	var date_seasonago =  new Date(date_today.getTime() - 90*24*60*60*1000);
	var date_yearago =  new Date(date_today.getTime() - 365*24*60*60*1000);

	zeropoint = " 00:00:00";
	endpoint = " 23:59:59";
	var date_today_str = date_today.format("yyyy-MM-dd") + zeropoint;

	//day
	day_start_str =  date_today.format("yyyy-MM-dd") + zeropoint;
	day_end_str = date_today.format("yyyy-MM-dd hh:mm:ss");
	//week
	week_start_str = date_weekago.format("yyyy-MM-dd") + zeropoint;
	week_end_str = date_today_str
	//month
	month_start_str = date_monthago.format("yyyy-MM-dd") + zeropoint;
	month_end_str = date_today_str;
	//season
	season_start_str = date_seasonago.format("yyyy-MM-dd") + zeropoint;
	season_end_str = date_today_str;
	//year
	year_start_str = date_yearago.format("yyyy-MM-dd") + zeropoint;
	year_end_str = date_today_str;
}

//format data for highcharts
function dataFormat(data) {
	var dataname = new Array();
	for(var o in data) {
		var datapoint = [Number(dateUTC(data[o].date)),Number(data[o].value)];
		dataname[dataname.length] = datapoint;
	}
	return dataname;
}

//-------------------Date Format--------------------//
Date.prototype.format = function(format){ 
	var o = { 
		"M+" : this.getMonth()+1, //month 
		"d+" : this.getDate(), //day 
		"h+" : this.getHours(), //hour 
		"m+" : this.getMinutes(), //minute 
		"s+" : this.getSeconds(), //second 
		"q+" : Math.floor((this.getMonth()+3)/3), //quarter 
		"S" : this.getMilliseconds() //millisecond 
	} 

	if(/(y+)/.test(format)) { 
		format = format.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length)); 
	} 

	for(var k in o) { 
		if(new RegExp("("+ k +")").test(format)) { 
			format = format.replace(RegExp.$1, RegExp.$1.length==1 ? o[k] : ("00"+ o[k]).substr((""+ o[k]).length)); 
		} 
	} 
	return format; 
} 
