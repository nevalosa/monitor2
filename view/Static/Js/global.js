
//-- Time Variables --//

//yesterday
var yesterday_start_str;
var yesterday_end_str;
//day
var day_start_str;
var day_end_str;
//week
var week_start_str;
var week_end_str;
//month
var month_start_str;
var month_end_str;
//season
var season_start_str
var season_end_str;
//year
var year_start_str;
var year_end_str;


//-- Charts --//
// Used for charts.js which define the ajaxURL module name !!!
var ajaxModuleName="AjaxUserData";


//-- Public Functions --//

//Function to convert hex format to a rgb color
	/*RGB to Hex*/
	var hexDigits = new Array("0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"); 
	function rgb2hex(rgb) {
		rgb = rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
		return "#" + hex(rgb[1]) + hex(rgb[2]) + hex(rgb[3]);
	}
	function hex(x) {
		return isNaN(x) ? "00" : hexDigits[(x - x % 16) / 16] + hexDigits[x % 16];
	}