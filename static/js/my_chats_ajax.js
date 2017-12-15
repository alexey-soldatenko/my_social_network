function getCookie(name){

    var matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ))
    return matches ? decodeURIComponent(matches[1]) : undefined
}


	
function show_chat(chat, author, companion, last_date){
    
    var wrap = document.getElementById('wrap');
    var box = document.getElementById('message-box')
    wrap.style.display = 'block';
    message_count_symbol();

    date_last_change = last_date;

    var form = document.forms.message_form;
    var chat_id = form.elements.chat_id;
    var author_id = form.elements.author_id;
    var companion_id = form.elements.companion_id;

    chat_id.value = chat;
    author_id.value = author;
    companion_id.value = companion; 
    


    httpRequest = new XMLHttpRequest();
    data = "chat_id=" + encodeURIComponent(chat) + "&mode=0";
    httpRequest.open("POST", "/my_chats", true);

    var csrf = getCookie('csrftoken');

    httpRequest.setRequestHeader("X-CSRFToken", csrf);
 
    httpRequest.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
 
    httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');

    httpRequest.onreadystatechange = function(){
        if (httpRequest.readyState == 4 && httpRequest.status == 200){
        var overflow_block = document.getElementById('overflow-message-block');
        overflow_block.innerHTML = httpRequest.responseText;
        overflow_block.scrollTop = overflow_block.scrollHeight;
        }
    };

    httpRequest.send(data);
}


function create_ajax_request(){

    var form = document.forms.message_form;
    var chat_id = form.elements.chat_id.value;
    var author_id = form.elements.author_id.value;
    var companion_id = form.elements.companion_id.value;
    var message_text = form.elements.message_text.value;

    var data = "chat_id=" + encodeURIComponent(chat_id) + "&author_id="+ encodeURIComponent(author_id) + "&companion_id=" + encodeURIComponent(companion_id)+ "&message_text=" + encodeURIComponent(message_text) + "&last_date=" + encodeURIComponent(date_last_change) + "&mode=1"
        ;
    
    var httpRequest = new XMLHttpRequest();
    httpRequest.open("POST", "/my_chats", true);

    var csrf = getCookie('csrftoken');

    httpRequest.setRequestHeader("X-CSRFToken", csrf);
 
    httpRequest.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
 
    httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
  
    
    httpRequest.onreadystatechange = function(){
        if (httpRequest.readyState == 4 && httpRequest.status == 200){

            var data = JSON.parse(httpRequest.responseText); 
            date_last_change = data["new_date"]; 
           
            var overflow_block = document.getElementById('overflow-message-block');
            overflow_block.innerHTML += data["ajax_response"];
            overflow_block.scrollTop = overflow_block.scrollHeight; 

            }
        };
 
    httpRequest.send(data);
 
}

function review_new_message(){
    var div_wrap = document.getElementById('wrap');
    if (div_wrap.style.display == 'block'){

        var form = document.forms.message_form;
        var chat_id = form.elements.chat_id.value;

        var data = "chat_id=" + encodeURIComponent(chat_id) + "&last_date=" + encodeURIComponent(date_last_change)+ "&mode=2";

        var httpRequest = new XMLHttpRequest();

        httpRequest.open("POST", '/my_chats', true);

        var csrf = getCookie('csrftoken');

        httpRequest.setRequestHeader('X-CSRFToken', csrf);
        httpRequest.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');

        httpRequest.onreadystatechange = function(){
        if (httpRequest.readyState == 4 && httpRequest.status == 200){

            var data = JSON.parse(httpRequest.responseText); 
            date_last_change = data["new_date"]; 

            var overflow_block = document.getElementById('overflow-message-block');
            overflow_block.innerHTML += data["ajax_response"];
            overflow_block.scrollTop = overflow_block.scrollHeight; 

            }
        };

        httpRequest.send(data);
    }
}


/*функция для работы с ajax на jquery*/
/*
$(document).ready(function() {
            $("#button").click(function() {
                    var form = document.forms.message_form;
                    var chat_id = form.elements.chat_id.value;
                    var author_id = form.elements.author_id.value;
                    var companion_id = form.elements.companion_id.value;
                    var message_text = form.elements.message_text.value;

                    $.ajax({
                        url : "/my_chats", 
                        type : "POST",
                        dataType: "json", 
                        data : {
                            chat_id:chat_id,
                            author_id:author_id,
                            companion_id:companion_id,
                            message_text:message_text,
                            csrfmiddlewaretoken:'{{ csrf_token }}'
                            },
                        success : function(json) {
                            
                            var innerdiv1 = document.createElement('DIV');
                            var innerdiv2 = document.createElement('DIV');
                            var person_img = document.createElement('IMG');
                            var name = document.createElement('SPAN')
                            
                            if (json.user == '{{user.username}}'){
                                innerdiv1.className = 'my_name';
                                innerdiv2.className = 'my_message_text'; 
                                 
                            }
                            else{
                                innerdiv1.className = 'companion_name';
                                innerdiv2.className = 'companion_message_text';
                                
                            }
                            
                            var parentblock = document.getElementsByClassName('overflow-message-block')[0];

                            parentblock.appendChild(innerdiv1);
                            parentblock.appendChild(innerdiv2);

                            person_img.src = json.user_image;
                            name.innerHTML = json.user + ":";
                            innerdiv1.appendChild(person_img);
                            innerdiv1.appendChild(name);
                            innerdiv2.innerHTML = json.text;
      
                        },
                        error : function(xhr,errmsg,err) {
                            alert(xhr.status + ": " + xhr.responseText);
                        }
                    });
                    return false;
            });
        });
*/