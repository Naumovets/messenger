window.addEventListener('load', function() {
    var yourDiv = document.getElementById('chat');
    yourDiv.scrollTop = yourDiv.scrollHeight;

    longpoll();
});



function send(e){
    var yourDiv = document.getElementById('chat');
    yourDiv.scrollTop = yourDiv.scrollHeight;
    e.preventDefault();
    var servResponse = document.querySelector('#chat');
    var id = document.location.pathname.split('/')[2]
    var text = document.forms.messageForm.message.value;
    formData = 'id='+ encodeURIComponent(id) +"&text="+encodeURIComponent(text);
    var xhr = new XMLHttpRequest();

    xhr.open('POST','/api/v1/long-poll',true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    xhr.setRequestHeader('X-CSRFToken',getCookie('csrftoken'));
    xhr.onreadystatechange = function(){

        if(xhr.readyState === 4 && xhr.status === 200){
            data = JSON.parse(xhr.response);
            let div = document.createElement('div');
            div.className = "col d-flex justify-content-end";
            div.innerHTML = '<div class="message m-2  ps-3 pt-2 pe-3 pb-2">\
                                <h5 class="m-0">' + data.name + ' ' + data.lastname +'</h5>\
                                <p class="m-0">' + text + '</p>\
                            </div>';
            flag = false;

            if (yourDiv.scrollTop + 500 > yourDiv.scrollHeight){
                flag = true;
            }
            document.forms.messageForm.message.value = '';
            servResponse.append(div);
            if(flag){
                yourDiv.scrollTop = yourDiv.scrollHeight;
            }
        }
    }

    xhr.send(formData);
}



function longpoll(){
    var yourDiv = document.getElementById('chat');
    var servResponse = document.querySelector('#chat');
    var id = document.location.pathname.split('/')[2]
    formData = 'id='+ encodeURIComponent(id);
    var dhr = new XMLHttpRequest();

    dhr.open('POST','/api/v1/check-message',true);
    dhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    dhr.setRequestHeader('X-CSRFToken',getCookie('csrftoken'));
    dhr.onreadystatechange = function(){

        if(dhr.readyState === 4 && dhr.status === 200){
            data = JSON.parse(dhr.response).data;
            for(var i = 0; i< data.length; i++){
                let div = document.createElement('div');
                div.className = "col d-flex justify-content-start";
                div.innerHTML = '<div class="message m-2  ps-3 pt-2 pe-3 pb-2">\
                                    <h5 class="m-0">' + data[i].from_user__first_name + ' ' + data[i].from_user__last_name +'</h5>\
                                    <p class="m-0">' + data[i].text + '</p>\
                                </div>';
                flag = false;

                if (yourDiv.scrollTop + 500 > yourDiv.scrollHeight){
                    flag = true;
                }
                document.forms.messageForm.message.value = '';
                servResponse.append(div);
                if(flag){
                    yourDiv.scrollTop = yourDiv.scrollHeight;
                }
            }
            longpoll();

        }
    }

    dhr.send(formData);
}



function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}