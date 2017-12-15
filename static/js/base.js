function show_login_block(evt){
		//сбрасываем настройки строки поиска
		var s = document.getElementById("search");
		s.style.border = "2px solid white";
		s.style.background = "#DCDCDC";

		//блок для входа 
		var show_block = document.getElementById("login-block");
		if (show_block.style.display != "block"){
			var log_link = document.getElementById("login-link");
			var coords = log_link.getBoundingClientRect();
			try{
				var coord_left = document.getElementsByClassName("other-info")[0].getBoundingClientRect().left;
			}
			catch(err){
				
			}
			
			show_block.style.display = "block";
			show_block.style.right = screen.width - coords.right -15 + "px";
			show_block.style.left = coord_left + "px";
			show_block.style.top = coords.bottom + 25 +"px";
		}
		else{
			show_block.style.display = "none";
		}

		//запрещаем дальнейшую обработку события onclick для родительских элементов
		evt.stopPropagation();
    	
		
	}

	function pass_func(evt){
		//запрещаем дальнейшую обработку события onclick для родительских элементов
		evt.stopPropagation();

	}


	function click_event(param){
		var show_block = document.getElementById("login-block");
		show_block.style.display = "none";	

		var s = document.getElementById("search");
		s.style.border = "2px solid white";
		s.style.background = "#DCDCDC";
		
	}

	function search_style(evt){
		//настройка поисковой строки
		var s = document.getElementById("search");
		s.style.border = "2px solid #0082A4";
		s.style.background = "white";


		var show_block = document.getElementById("login-block");
		show_block.style.display = "none";	

		//запрещаем дальнейшую обработку события onclick для родительских элементов
		evt.stopPropagation();
    	
	}

	function show_add_comment_form(record, author){
		var record_form = document.getElementById('Wrap1');
		var rec = document.getElementById('comment-form');
		record_form.style.display = 'block';
		count_symbol();

		var comment = document.forms.comment;
		var record_id = comment.elements.record_id;
		var author_email = comment.elements.author_record;

		record_id.value = record;
		author_email.value = author;
		
		
	}

	function close_add_comment_form(){
		var record_form = document.getElementById('Wrap1');
		record_form.style.display = 'none';
	}

	function count_symbol(){
    	var text_area = document.getElementById('text_area');
    	var counter = document.getElementById('counter');
    	var text_len = text_area.value.length;
    	counter.innerHTML = text_len + '/140'
    }

    function show_comments(id_name, verb_name){
    	var comments = document.getElementById(id_name);
    	var verbose_comment = document.getElementById(verb_name);
    	if (comments.style.display == 'none'){
    		comments.style.display = 'block';
    		verbose_comment.innerHTML = 'Скрыть комментарии:';
    	}
    	else{
    		comments.style.display = 'none';
    		verbose_comment.innerHTML = 'Комментарии:';
    	}
    }

function getCookie(name){

    var matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ))
    return matches ? decodeURIComponent(matches[1]) : undefined
}



function ajax_meta_request(method, record){
	if (method == 'like'){
		var data = "record_id=" + encodeURIComponent(record);

		var httpRequest = new XMLHttpRequest();
		var csrftoken = getCookie('csrftoken');

		httpRequest.open('POST', '/add_like', true);

		httpRequest.setRequestHeader('X-CSRFToken', csrftoken);
		httpRequest.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
		httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
		var id_elem = 'like_record_'+record;

		httpRequest.onreadystatechange = function(){
			if (httpRequest.readyState == 4 && httpRequest.status == 200){

				var count_like = document.getElementById(id_elem);
				count_like.innerHTML = " " + httpRequest.responseText;

			}
		};

		httpRequest.send(data);
	}

	else if (method == 'repost'){
		var data = "record_id=" + encodeURIComponent(record);

		var httpRequest = new XMLHttpRequest();
		var csrftoken = getCookie('csrftoken');

		httpRequest.open('POST', '/add_repost', true);

		httpRequest.setRequestHeader('X-CSRFToken', csrftoken);
		httpRequest.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
		httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
		var id_elem = 'repost_record_'+record;

		httpRequest.onreadystatechange = function(){
			if (httpRequest.readyState == 4 && httpRequest.status == 200){

				var count_like = document.getElementById(id_elem);
				count_like.innerHTML = " " + httpRequest.responseText;

			}
		};

		httpRequest.send(data);
	}
}


function ajax_message_request(){
	var comment = document.forms.comment;
	var record_id = comment.elements.record_id;
	var comment_text = comment.elements.comment_text;

	data = "record_id=" + encodeURIComponent(record_id.value) + "&comment_text=" + encodeURIComponent(comment_text.value);

	var httpRequest = new XMLHttpRequest();
	var csrftoken = getCookie('csrftoken');

	httpRequest.open('POST', '/add_comment', true);

	httpRequest.setRequestHeader('X-CSRFToken', csrftoken);
	httpRequest.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
	var id_elem = 'comment_record_' + record_id.value;
	var count_id = 'comment_count_record_' + record_id.value;

	httpRequest.onreadystatechange = function(){
		if (httpRequest.readyState == 4 && httpRequest.status == 200){
			try{
				var comment_block = document.getElementById(id_elem);
				var count_comment = document.getElementById(count_id)
				var data = JSON.parse(httpRequest.responseText);
				comment_block.innerHTML +=  data["html_text"];
				count_comment.innerHTML = data["count_comments"];

			var record_form = document.getElementById('Wrap1');
			record_form.style.display = 'none';

			var comm_name = 'comments_'+record_id.value;
			var verb_name =  'verb_' + record_id.value;
			var comments = document.getElementById(comm_name);

	    	var verbose_comment = document.getElementById(verb_name);
	    	if (comments.style.display == 'none'){
	    		comments.style.display = 'block';
	    		verbose_comment.innerHTML = 'Скрыть комментарии:';
	    	}
	    	
				}

			catch(err){
				alert(err);
			}
			
			}
		};

	httpRequest.send(data);
}