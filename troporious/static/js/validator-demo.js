var secret = null;

$(document).ready(function() {
    var button_call = $('#button_call');
    $('#button_call').click(function() {
        $(this).attr('disabled', 'disabled');
        var target = 'tel:'+$('#input_phone').val();
        $.get(
          '/validate',
          {
            api_key:'e890832202767ae59832aed8338a62df',
            target:'tel:'+$('#input_phone').val()
          },
          function(data) {
            var obj = JSON.parse(data);
            secret = obj.secret;
          });
    });
    
    $('#button_check').click(function() {
        if ($('#input_secret').val() == secret) {
          alert('correct!');
        }
        else {
          alert('wrong!');
        }
    });
});
