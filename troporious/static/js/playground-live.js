function sendMessage(opt_param) {
  var path = '/playground-live?from=client&session_id='+session_id+'&';
  path += opt_param;
  var xhr = new XMLHttpRequest();
  xhr.open('POST', path, true);
  xhr.send();
}
var timeout = 30;
function onTick() {
    $('#timeout').html(timeout);
    if (timeout !== 0) {
        timeout = timeout - 1;
        setTimeout(onTick, 1000);
    }
    else {
        $('#timeout').html('Script is over!');
    }
}
$(document).ready(function() {
        var debug_window = $('#debug-window');
        var start_form = $('#start-form');
        var init_disabled = $('.init_disabled').children();
        init_disabled.attr('disabled','disabled');
        var init_hidden = $('.init_hidden');
        init_hidden.hide();
        function debug_msg(msg) {
            debug_window.html( debug_window.html() + msg + '<br>');
        }
        $('#toggle_debug').click(function() {
                debug_window.toggle();
        });
        $('#btn_start').click(function() {
                url = '/playground-live?action=new&number='+encodeURIComponent($('#phone_number').val());
                if ($('#live_audio').attr('checked')) {
                    url += '&live-audio=true';
                }
                $.get(url, function(data) {
                        response = JSON.parse(data);
                        window.session_id = response['session_id'];
                        window.channel_token = response['channel_token'];
                        channel = new goog.appengine.Channel(channel_token);
                        socket = channel.open();
                        socket.onopen = function() {
                            debug_msg('channel connection opened');
                        };
                        socket.onmessage = function(data) {
                            response = JSON.parse(data.data);
                            if (response['type'] == 'msg') {
                                debug_msg('recieved : ' + response['msg']);
                            }
                            else if (response['type'] == 'recording') {
                                debug_msg('a recording. will try to play it.');
                                $('embed').remove();
                                $('body').append('<embed src="'+response['file_link']+'" autostart="true" hidden="true" loop="false">');
                            }
                        };
                        socket.onerror = function() {
                            debug_msg('channel error occured');
                        };
                        socket.onclose = function() {
                            debug_msg('channel connection closed');
                        };
                        init_hidden.show();
                        start_form.hide();
                        onTick();
                });
        });
        $('#exec').click(function() {
                var code = $('#code').val();
                var action = { 'action' : 'exec', 'code' : code };
                sendMessage('action='+JSON.stringify(action));
        });
        $('#say').click(function() {
                var text = $('#say_text').val();
                var action = { 'action' : 'say', 'text' : text };
                sendMessage('action='+JSON.stringify(action));
        });
        $('#transfer_yes').click(function() {
                init_disabled.attr('disabled','');
        });
        $('#transfer_no').click(function() {
                init_disabled.attr('disabled', 'disabled');
        });
});
