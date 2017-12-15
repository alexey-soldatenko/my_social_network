function show_message_box(){
  
		var wrap = document.getElementById('wrap');
		var box = document.getElementById('message-box')
		wrap.style.display = 'block';
		message_count_symbol();

	}

	function close_message_box(){
		var wrap = document.getElementById('wrap');
		wrap.style.display = 'none';
		var overflow_block = document.getElementById('overflow-message-block');
        overflow_block.innerHTML = "";
	}

    function message_count_symbol(){
    	var text_area = document.getElementById('message_textarea');
    	var counter = document.getElementById('message_counter');
    	var text_len = text_area.value.length;
    	counter.innerHTML = text_len + '/250'
    }


