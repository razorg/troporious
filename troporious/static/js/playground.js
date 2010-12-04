function sendMessage(opt_param) {
  var path = '/playground-live?';
  path += opt_param;
  var xhr = new XMLHttpRequest();
  xhr.open('POST', path, true);
  xhr.send();
}

$(document).ready(function() {
        var init_disabled = $('.init_disabled').children();
        init_disabled.attr('disabled','disabled');
        var init_hidden = $('.init_hidden');
        init_hidden.hide();
        $('#btn_start').click(function() {
                $.get('/playground-live?action=new&channel_token='+channel_token, function(data) {
                        window.session_id = data;
                        init_hidden.show();
                        $('#btn_start').hide();
                });
        });
        $('#btn_call').click(function() {
                var num = $('#input_phone_num').val();
                var action_str = 'method:call,num:'+num;
                sendMessage('from=client&'+'channel_token='+channel_token+'&session_id='+session_id+'&action='+encodeURIComponent(action_str));
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
    alert('onOpened');
}
function onMessage(msg) {
    alert('recieved : ' + msg.data);
}
function onError() {
    alert('onError');
}
function onClose() {
    alert('onClose');
}
