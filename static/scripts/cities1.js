var state_arr = new Array('Andhra Pradesh', 'Assam', 'Bihar', 'Gujarat', 'Karnataka',
       'Madhya Pradesh', 'Maharashtra', 'Meghalaya', 'Mizoram', 'Punjab',
       'Rajasthan', 'Telangana', 'Uttar Pradesh', 'Haryana', 'Nagaland',
       'West Bengal', 'Tamil Nadu', 'Manipur', 'Goa', 'Arunachal Pradesh',
       'Jammu and Kashmir', 'Odisha', 'Chandigarh',
       'Dadra and Nagar Haveli', 'Himachal Pradesh', 'Tripura',
       'Puducherry', 'Sikkim', 'Kerala', 'Chhattisgarh', 'Uttarakhand',
       'Andaman and Nicobar Islands', 'Jharkhand');


function print_state(state_id){
	// given the id of the <select> tag as function argument, it inserts <option> tags
	var option_str = document.getElementById(state_id);
	option_str.length=0;
	option_str.options[0] = new Option('Select State','');
	option_str.selectedIndex = 0;
	for (var i=0; i<state_arr.length; i++) {
		option_str.options[option_str.length] = new Option(state_arr[i],state_arr[i]);
	}
}

