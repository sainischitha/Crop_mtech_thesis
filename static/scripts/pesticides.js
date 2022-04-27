var pesticide_arr = new Array('Insecticides', 'Bactericides', 'Herbicides');


function print_pesticide(pesticide_id){
	// given the id of the <select> tag as function argument, it inserts <option> tags
	var option_str = document.getElementById(pesticide_id);
	option_str.length=0;
	option_str.options[0] = new Option('Select Pesticide','');
	option_str.selectedIndex = 0;
	for (var i=0; i<pesticide_arr.length; i++) {
		option_str.options[option_str.length] = new Option(pesticide_arr[i],pesticide_arr[i]);
	}
}

