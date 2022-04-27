var newseason_arr = new Array('Summer', 'Monsoon', 'Winter');


function print_newseason(newseason_id){
	// given the id of the <select> tag as function argument, it inserts <option> tags
	var option_str = document.getElementById(newseason_id);
	option_str.length=0;
	option_str.options[0] = new Option('Select Season','');
	option_str.selectedIndex = 0;
	for (var i=0; i<newseason_arr.length; i++) {
		option_str.options[option_str.length] = new Option(newseason_arr[i],newseason_arr[i]);
	}
}

