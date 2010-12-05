function sendMessage(opt_param) {
  var path = '/playground-live?';
  path += opt_param;
  var xhr = new XMLHttpRequest();
  xhr.open('POST', path, true);
  xhr.send();
}
var timeout = 30;
function onTick() {
    $('#timeout').html(timeout);
    if (timeout != 0) {
        timeout = timeout - 1;
        setTimeout("onTick()", 1000);
    }
    else {
        $('#timeout').html('Script is over!');
    }
}
$(document).ready(function() {
        var init_disabled = $('.init_disabled').children();
        init_disabled.attr('disabled','disabled');
        var init_hidden = $('.init_hidden');
        init_hidden.hide();
        $('#btn_start').click(function() {
                $.get('/playground-live?action=new', function(data) {
                        response = JSON.parse(data);
                        window.session_id = response['session_id'];
                        window.channel_token = response['channel_token'];
                        channel = new goog.appengine.Channel(channel_token);
                        socket = channel.open();
                        socket.onopen = onOpened;
                        socket.onmessage = onMessage;
                        socket.onerror = onError;
                        socket.onclose = onClose;
                        init_hidden.show();
                        $('#btn_start').hide();
                        onTick();
                });
        });
        $('#btn_call').click(function() {
                var num = $('#input_phone_num').val();
                var action_str = 'method:call,num:'+num;
                sendMessage('from=client'+'&session_id='+session_id+'&action='+encodeURIComponent(action_str));
        });
        $('#transfer_yes').click(function() {
                init_disabled.attr('disabled','');
        });
        $('#transfer_no').click(function() {
                init_disabled.attr('disabled', 'disabled');
        });
});
function socket_debug_msg(msg) {
    $('#socket-debug').html( $('#socket-debug').html() + msg + '<br>');
}
function onOpened() {
    socket_debug_msg('onOpened');
}
function onMessage(msg) {
    socket_debug_msg('recieved : ' + msg.data);
}
function onError() {
    socket_debug_msg('onError');
}
function onClose() {
    socket_debug_msg('onClose');
}
