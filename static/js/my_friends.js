function show_new_message_form(companion, author){
		var message_form = document.getElementById('Wrap2');
		var rec = document.getElementById('message-form');
		message_form.style.display = 'block';

		var form = document.forms.new_message_form;
		form.elements.companion_id.value = companion;
		form.elements.author_id.value = author

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