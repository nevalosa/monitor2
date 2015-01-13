var SideNavStatus={};

$(".nav-sidebar .nav-list").click(function(){
	// open link
	sideNavParam = "";
	for(key in SideNavStatus){
		if(SideNavStatus[key] == 'on')
		{
			if(sideNavParam == "")
				sideNavParam += key;
			else
				sideNavParam += ',' + key;
		}
		
	}
	if(sideNavParam != ""){
		url = this.href + "?SideNavStatus=" + sideNavParam;
	}
	else{
		url = this.href;
	}
	window.location.href=url;
	
});

function initSideNavStatus(){
	$(".nav-sidebar li ul").each(function(optIndex,optElement ){
		saveSideNaveStatus(optElement);
	});
	
	$(".nav-sidebar .nav-list").each(function(optIndex,optElement ){
		$(optElement).attr('onclick','return false;');
	});
}

function saveSideNaveStatus(obj){
	navkey = $(obj).attr('id');
	
	//console.log($(obj).hasClass('in'));
	if($(obj).hasClass('in')==true)
		SideNavStatus[navkey] = 'on';
	else
		SideNavStatus[navkey] = 'off';
}