var soiltype_arr = new Array('Alluvial', 'Black-Cotton');


function print_soiltype(soiltype_id){
	// given the id of the <select> tag as function argument, it inserts <option> tags
	var option_str = document.getElementById(soiltype_id);
	option_str.length=0;
	option_str.options[0] = new Option('Select SoilType','');
	option_str.selectedIndex = 0;
	for (var i=0; i<soiltype_arr.length; i++) {
		option_str.options[option_str.length] = new Option(soiltype_arr[i],soiltype_arr[i]);
	}
}

