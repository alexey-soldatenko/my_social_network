function click_event(param){
		var s = document.getElementById("search");
		s.style.border = "2px solid white";
		s.style.background = "#DCDCDC";

	
	}

	function search_style(evt){
		//настройка поисковой строки
		var s = document.getElementById("search");
		s.style.border = "2px solid #0082A4";
		s.style.background = "white";

		//запрещаем дальнейшую обработку события onclick для родительских элементов
		evt.stopPropagation();
    	
	}

	function file_input(param){
		var file_box = document.getElementById("Wrap1");

		var edit_box = document.getElementById("Wrap2");

		if (param == "Wrap1"){
			file_box.style.display = "block";  
			edit_box.style.display = "none";
		}
		else if (param == "Wrap2"){
			file_box.style.display = "none";  
			edit_box.style.display = "block";
		}	

	}

	

	function close_file_input(param){
		var file_box = document.getElementById("Wrap1");

		var edit_box = document.getElementById("Wrap2");

		if (param == "Wrap1"){
			file_box.style.display = "none";  
		}
		else if (param == "Wrap2"){ 
			edit_box.style.display = "none";
		}
	
	}
