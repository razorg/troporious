function sendMessage(opt_param) {
  var path = '/PlaygroundBackend?from=client&session_id='+session_id+'&';
  path += opt_param;
  var xhr = new XMLHttpRequest();
  xhr.open('POST', path, true);
  xhr.send();
}

function TropoQueue(element) {
    this.dom = element;
    this.empty = true;
    this.started = false;
    this.init_signal = $('#signals');
    this.action_array = new Array();
}
TropoQueue.prototype.addAction = function(action, html) {
    if (this.empty) {
        this.dom.html('');
        this.empty = false;
    }
    if (this.started) {
        this.enqueue_backend(action);
    }
    this.action_array[this.action_array.length] = action;
    this.dom.html(this.dom.html() + html);
}
TropoQueue.prototype.start = function(init_num) {
    var self = this;
    $.get('/StartSession?init_number='+encodeURIComponent(init_num), function(data) {
            alert(data);
            self.init_signal.trigger('start', data);
    });
}
TropoQueue.prototype.init_enqueue_backend = function() {
    for (i in this.action_array) {
        var elem = this.action_array[i];
        sendMessage('action='+JSON.stringify(elem));
    }
    this.started = true;
}
TropoQueue.prototype.enqueue_backend = function(action) {
    sendMessage('action='+JSON.stringify(action));
}
TropoQueue.prototype.dequeue_only = function() {
    this.action_array.splice(0,1);
    $('#queue div:first').remove();
}

$(document).ready(function() {
        var init_disabled = $('.init_disabled').children();
        var queue = new TropoQueue($('#queue'));
        init_disabled.attr('disabled','disabled');
        var debug_window = $('#debug_window');
        function debug_msg(msg) {
            debug_window.html( debug_window.html() + msg + '<br>');
        }
        $('#transfer_yes').click(function() {
                init_disabled.attr('disabled','');
        });
        $('#transfer_no').click(function() {
                init_disabled.attr('disabled', 'disabled');
        });
        
        $('#btn_add_say').click(function() {
                new_action = {'action':'say','text':$('#say_text').val()};
                queue.addAction(new_action, '<div class="queue_elem border queue_say"> SAY : '+$('#say_text').val()+'</div>');
        });
        $('#btn_add_transfer').click(function() {
                new_action = {'action':'transfer','number':encodeURIComponent($('#transfer_number').val())};
                queue.addAction(new_action, '<div class="queue_elem border queue_transfer"> TRANSFER TO '+$('#transfer_number').val()+'</div>');
        });
        $('#btn_start').click(function() {
                queue.start($('#init_number').val());
        });
        queue.init_signal.bind('start', function(e, data) {
                response = JSON.parse(data);
                window.session_id = response['session_id'];
                window.channel_token = response['channel_token'];
                channel = new goog.appengine.Channel(channel_token);
                socket = channel.open();
                socket.onopen = function() {
                    debug_msg('channel connection opened');
                    queue.init_enqueue_backend();
                };
                socket.onmessage = function(data) {
                    response = JSON.parse(data.data);
                    if (response['type'] == 'msg') {
                        if (response['what'] == 'dequeue') {
                            queue.dequeue_only();
                        }
                        debug_msg('recieved : ' + response['msg']);
                    }
                    else {
                        alert('adada');
                    }
                };
                socket.onerror = function() {
                    debug_msg('channel error occured');
                };
                socket.onclose = function() {
                    debug_msg('channel connection closed');
                };
        });
});                    
