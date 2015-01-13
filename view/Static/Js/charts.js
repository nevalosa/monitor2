
// Global Chart Data Cache
var ChartDataCache={};
/*
ChartDataCache['172.172.172.18_daystart_dayend_siponlineuser']={
        name: 'data1',
        data: [
			[Date.UTC(2015,  1, 4,10,0,0), 1   ],
			[Date.UTC(2015,  1, 4,11,0,0), 10   ],
			[Date.UTC(2015,  1, 4,12,0,0), 100  ],
			[Date.UTC(2015,  1, 4,13,0,0), 1000   ],
        ]
	};
*/



//ajax rewrite chart
function rewriteChart(){
	// Get ajax link params (jSon Format)
	var chartParam=getChartParams();
	
	// Get series data
	var seriesVal=[];
	$("#ajaxOptions :checkbox").each(function(optIndex,optElement ){
		if(optElement.checked == true){
			
			if( $("#ajaxHost :checkbox").length ==0 )
			{
				//Get Data Cache's Key
				combineKey = optElement.value + chartParam['start'] +  chartParam['end'];
				//if  Data Cache not exists, get value from ajax
				if(typeof(ChartDataCache[combineKey])=="undefined"){
					//get data
					ajaxData=requestAjax('/index.php/'+ajaxModuleName+'/'+optElement.value,
						getChartParams(), dataFormat);
					//get color
					//console.log(optElement);
					rgbColor = $(optElement).parent().css('color');
					hexColor = rgb2hex(rgbColor);
					//set cache
					ChartDataCache[combineKey]={
					        name: optElement.value,
					        color: hexColor,
					        //symbol: 'circle', //circle/square/diamond/triangle/triangle-down"
					        data: ajaxData
						};
					//set data
					seriesVal.push(ChartDataCache[combineKey]);
				}
				//Data Cache exists, add it to the 'Chart Series'
				else{ 
					seriesVal.push(ChartDataCache[combineKey]);
				}
			}
			else
			{	// with multiple hosts
				/*
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
				*/
			}
		}
	});
	
	//Other config
	yAxis_title = $('#realTimeChart').attr('yAxis_title');
	
	//run real time chart
	realTimeChart(seriesVal, yAxis_title);
	
	//run other chart
	
	
	return true;
}

function realTimeChart(seriesVal, yAxis_title){
	// Set Chart Style
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
            type: 'spline',                         //指定图表的类型，默认是折线图（line）
        },
        plotOptions: {
        	spline: {
                lineWidth: 2,
                states: {
                    hover: {
                        lineWidth: 3
                    }
                },
                marker: {
                    enabled: false,
                    symbol:"circle"
                }
            }
        },
        title: {
            text: 'My first Highcharts chart'      //指定图表标题
        },
        tooltip: {
            crosshairs: [true]
        },
        xAxis: { 
        	type: 'datetime',
        	dateTimeLabelFormats:{
        		millisecond: '%H:%M:%S.%L',
        		second: '%H:%M:%S',
        		minute: '%H:%M',
        		hour: '%H:%M',
        		day: '%b %d',
        		week: '%y-%m-%d',
        		month: '%b \'%y',
        		year: '%Y'
        	},
        },
        title: {
            text: 'Date'
        },
        yAxis: {
            title: {
                text: yAxis_title                  //指定y轴的标题
            },
            //min: 0
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

//Get Chart Params for Ajax
function getChartParams(){
	//variables
	paramStart="";
	paramEnd="";
	paramType="";
	
	//Get checked date picker radio.
	date_checked=$("#ajaxDatePicker :radio:checked")[0];
	
	//Set Start and End Time: xxxx-xx-xx xx:xx:xx
	switch(date_checked.value)
	{
		case 'today':
			paramType="normal";
			paramStart=day_start_str;
			paramEnd=day_end_str;
			break;
		case 'yesterday':
			paramType="normal";
			paramStart=yesterday_start_str;
			paramEnd=yesterday_end_str;
			break;
		case 'week':
			paramType="day";
			paramStart=week_start_str;
			paramEnd=week_end_str;
			break;
		case 'month':
			paramType="day";
			paramStart=month_start_str;
			paramEnd=month_end_str;
			break;
		case 'season':
			paramType="week";
			paramStart=season_start_str;
			paramEnd=season_end_str;
			break;
		case 'year':
			paramType="month";
			paramStart=year_start_str;
			paramEnd=year_end_str;
			break;
		case 'range':
			paramType="normal";
			inStart=$('#datepicker :input')[0];
			inEnd=$('#datepicker :input')[1];
			paramStart=inStart.value + " 00:00:00";
			paramEnd=inEnd.value + " 00:00:00";
			break;
		default:
			paramType="normal";
			paramStart=day_start_str;
			paramEnd=day_end_str;
			break;
	}
	
	
	params = {
		"type":"normal",
		"start":paramStart,
		"end":paramEnd
	}

	return params
}

//calculate time range
function calculateDate(){
	var date_today = new Date();
	var date_dayago =  new Date(date_today.getTime() - 1*24*60*60*1000);
	var date_weekago =  new Date(date_today.getTime() - 7*24*60*60*1000);
	var date_monthago =  new Date(date_today.getTime() - 30*24*60*60*1000);
	var date_seasonago =  new Date(date_today.getTime() - 90*24*60*60*1000);
	var date_yearago =  new Date(date_today.getTime() - 365*24*60*60*1000);

	zeropoint = " 00:00:00";
	endpoint = " 23:59:59";
	var date_today_str = date_today.format("yyyy-MM-dd") + zeropoint;

	//yesterday
	yesterday_start_str=date_dayago.format("yyyy-MM-dd") + zeropoint;
	yesterday_end_str=date_today_str;
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
