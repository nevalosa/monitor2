//-------------------prepare data----------------------//
$(document).ready(function() {
	
	// -- Side Nav --//
	// Bind Click Event
	$(".nav-sidebar li ul").on('shown.bs.collapse', function () {
		saveSideNaveStatus(this);
	})
	$(".nav-sidebar li ul").on('hidden.bs.collapse', function () {
		saveSideNaveStatus(this);
	})
	//Set Side Nav Status for Init
	initSideNavStatus();
	
	// -- Chart --//
	// Set Time
	calculateDate();
	
	// Just run when there is a chart
	if($("#realTimeChart").length){
		// Bind Click Event
		$("#ajaxDatePicker :radio").click(function(){
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
	}
	
});
