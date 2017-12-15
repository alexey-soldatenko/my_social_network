function show_add_record_form(){
		var record_form = document.getElementById('Wrap');
		var rec = document.getElementById('record-form')
		record_form.style.display = 'block';
		count_symbol();
	}

	function close_add_record_form(){
		var record_form = document.getElementById('Wrap');
		record_form.style.display = 'none';
	}

	function show_name_file()
            {
                var file = document.getElementById('my_file').files[0];

                var file_name = document.getElementById('file_name');

                if (file.type.indexOf('image') == -1){
                	file_name.innerHTML = "Файл не является картинкой.";
                	file_name.style.color = 'red';
                    var form = document.forms.record_form;
                    form.elements.submit.disable = true;
                }

                else if (file.size > 200000){
                	file_name.innerHTML = "Максимальный размер файла 2 Мб.";
                	file_name.style.color = 'red';
                    var form = document.forms.record_form;
                    form.elements.submit.disabled = true;
                }
                else{
                	file_name.style.color = 'inherit';
                	var size = '';

                	if (file.size > 1000000){
                		size = (Math.floor(file.size/1000000)).toString() + 'Мб';
                		
                	}
                	else if (file.size > 1000){
                		
                		size = (Math.floor(file.size/1000)).toString() + 'Кб';
                		
                	}
                	else{
                		size = (file.size).toString() + 'б';
                	}

                	file_name.innerHTML = file.name + ' '+ size;
                }
                if (file.size < 2000000){
                    var form = document.forms.record_form;
                    form.elements.submit.disabled = false;
                }
              
                
            }

    function count_symbol(){
    	var text_area = document.getElementById('text_area');
    	var counter = document.getElementById('counter');
    	var text_len = text_area.value.length;
    	counter.innerHTML = text_len + '/250'
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