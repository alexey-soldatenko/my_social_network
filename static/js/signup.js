function show_login_block(evt){
		var show_block = document.getElementById("login-block");
		if (show_block.style.display != "block"){
			var log_link = document.getElementById("login-link");
			var coords = log_link.getBoundingClientRect();
			
			show_block.style.display = "block";
			show_block.style.right = screen.width - coords.right -15 + "px";
			show_block.style.top = coords.bottom + 25 +"px";
		}
		else{
			show_block.style.display = "none";
		}
		evt.stopPropagation();
    	
		
	}

	function pass_func(evt){
		evt.stopPropagation();
    	
	}


	function click_event(){
		
		var show_block = document.getElementById("login-block");
		show_block.style.display = "none";	
		
	}