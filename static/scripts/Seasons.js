var season_arr = new Array('Kharif', 'Rabi', 'Whole Year');


function print_season(season_id){
	// given the id of the <select> tag as function argument, it inserts <option> tags
	var option_str = document.getElementById(season_id);
	option_str.length=0;
	option_str.options[0] = new Option('Select Season','');
	option_str.selectedIndex = 0;
	for (var i=0; i<season_arr.length; i++) {
		option_str.options[option_str.length] = new Option(season_arr[i],season_arr[i]);
	}
}

