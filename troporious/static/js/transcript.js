function sendMessage(opt_param) {
  var path = '/transcript-callback?from=client&session_id='+session_id+'&';
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
        $('#btn-send').click(function() {
                $('#texta-send').focus();
                action = {'action':'send_message','msg':$('#texta-send').val()};
                sendMessage('action='+JSON.stringify(action));
                $('#texta-send').val('');
        });
        $('#call').click(function() {
                url = '/transcript-callback?action=new&number='+encodeURIComponent($('#phone').val());
                $.get(url, function(data) {
                        $('#page-phone').detach();
                        init_hidden.show();
                        response = JSON.parse(data);
                        window.session_id = response['session_id'];
                        window.channel_token = response['channel_token'];
                        channel = new goog.appengine.Channel(channel_token);
                        socket = channel.open();
                        socket.onmessage = function(data) {
                            response = JSON.parse(data.data);
                            if (response['type'] == 'msg') {
                                $('#text-conv').html( $('#text-conv').html() + response['msg'] + '<br>');
                            }
                        };
                        socket.onerror = function() {
                            alert('channel error occured');
                        };
                        socket.onclose = function() {
                            alert('channel connection closed');
                        };
                });
        });
});
