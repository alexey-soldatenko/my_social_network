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

	function button_style(param, event){
		var reg = document.getElementById("submit-reg");
		var sub_in = document.getElementById("submit-in");
		if (event == "mouseover"){
			if (param == "log"){
				sub_in.style.background = "#0082A4";
				sub_in.style.color = "white";
				sub_in.style.cursor = "pointer";

				reg.style.color = "black";
				reg.style.background = "white";
				reg.style.border = "2px solid #0082A4";

			}
			else if (param == "reg"){

				sub_in.style.background = "#0082A4";
				sub_in.style.color = "white";
				sub_in.style.cursor = "pointer";

				reg.style.color = "black";
				reg.style.background = "white";
				reg.style.border = "2px solid #0082A4";
			}
		}
		else if (event == "mouseout"){

			if (param == "log"){
				reg.style.background = "#0082A4";
				reg.style.color = "white";
				reg.style.cursor = "pointer";

				sub_in.style.color = "black";
				sub_in.style.background = "white";
				sub_in.style.border = "2px solid #0082A4";

			}
			else if (param == "reg"){

				reg.style.background = "#0082A4";
				reg.style.color = "white";
				reg.style.cursor = "pointer";

				sub_in.style.color = "black";
				sub_in.style.background = "white";
				sub_in.style.border = "2px solid #0082A4";
			}
		}
	}