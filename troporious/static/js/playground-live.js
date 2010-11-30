$(document).ready(function() {
        $('.init_hidden').hide();
        $('#init_live').click(function() {
                $.get('/playground-live?action=create', function(data) {
                        if (data == 'fail') {
                            alert('failed to load.');
                            return;
                        }
                        alert(data);
                        $('.init_hidden').show();
                        
                });
        });
});
