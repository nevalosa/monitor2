$('#datepicker').datepicker({
	    format: "yyyy-mm-dd",
	    todayBtn: "linked",
	    autoclose: true
	});

$('#datepicker').datepicker().on('show', function(e){
	if( $("#date_range")[0].checked!=true){
		$("#date_range")[0].checked = true
	}
});

$('#datepicker').datepicker().on('hide', function(e){
	thisId=this.id;
	inStart=$('#'+thisId+' :input')[0];
	inEnd=$('#'+thisId+' :input')[1];
	if(inStart.value && inEnd.value)
		rewriteChart();
});