var croptype_arr = new Array('Kharif', 'Rabi');


function print_croptype(croptype_id){
	// given the id of the <select> tag as function argument, it inserts <option> tags
	var option_str = document.getElementById(croptype_id);
	option_str.length=0;
	option_str.options[0] = new Option('Select CropType','');
	option_str.selectedIndex = 0;
	for (var i=0; i<croptype_arr.length; i++) {
		option_str.options[option_str.length] = new Option(croptype_arr[i],croptype_arr[i]);
	}
}

