function show_new_message_form(){
		var message_form = document.getElementById('Wrap2');
		var rec = document.getElementById('message-form');
		message_form.style.display = 'block';
		count_symbol_message();
	
	}

    function close_new_message_form(){
		var record_form = document.getElementById('Wrap2');
		record_form.style.display = 'none';
	}

	function count_symbol_message(){
    	var text_area = document.getElementById('text_area');
    	var counter = document.getElementById('counter');
    	var text_len = text_area.value.length;
    	counter.innerHTML = text_len + '/250'
    }