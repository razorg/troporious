$(document).ready(function() {
        var init_disabled = $('.init_disabled').children(); 
        init_disabled.attr('disabled','disabled');
        $('#transfer_yes').click(function() {
                init_disabled.attr('disabled','');
        });
        $('#transfer_no').click(function() {
                init_disabled.attr('disabled', 'disabled');
        });
        
});
