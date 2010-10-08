function submit_form() {
    var input_to = document.getElementById("id_to");
    var input_msg = document.getElementById("id_msg");
    var text_to = input_to.value;
    var text_msg = input_msg.value;
    var regex_to = /^\+\d{12}$/;
    var div_ul_errors = document.getElementById("div_ul_errors");
    div_ul_errors.innerHTML = "";
    if (!regex_to.test(text_to)) {
        div_ul_errors.innerHTML = "<li>Not a valid phone number.</li>";
    }
    else {
        //http://nickmilon.appspot.com/tropo/SMS?num=+3069XXXXXX&msg=FOO
        window.location = "http://cloudutl.appspot.com/sms/smsReq?msgToNum="+text_to+"&msgTxt="+unescape(encodeURIComponent(text_msg));
        div_ul_errors.innerHTML = "";
        document.getElementById("id_submit").disabled = true;
        //var data = { "to":text_to, "msg":text_msg };
        //var data_jsontext = JSON.stringify(data);
        //load_script("http://nickmilon.appspot.com/sms/?data="+encodeURIComponent(data_jsontext)+"&callback=grabJSONP");
    }
}
function notify_area() {
    var textarea = document.getElementById("id_msg");
    var chars = document.getElementById("id_chars");
    chars.innerHTML = 160 - textarea.value.length;
}

function load_script(url) {
    var new_script = document.createElement("script");
    new_script.type = 'text/javascript';
    new_script.src = url;
    document.getElementsByTagName("head")[0].appendChild(new_script); 
}
function reload() {
    window.location = window.location;
}
function grabJSONP(data) {
    var div_errors = document.getElementById("div_errors");
    var div_ul_errors = document.getElementById("div_ul_errors");
    if (data.code = 200) {
        div_errors.style.backgroundColor = '#58FA58';
        div_ul_errors.innerHTML = "<li>SMS has been sent.</li>";
    }
    else {
        div_ul_errors.innerHTML = "<li>Error while sending SMS. Please try again later.</li>";
    }
    var button_area = document.getElementById("id_button_area");
    var reload_button = document.createElement("button");
    reload_button.style.float = 'right';
    reload_button.className = 'button';
    reload_button.innerHTML = "reload!";
    reload_button.onclick = reload;
    button_area.appendChild(reload_button);
}
