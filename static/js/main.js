$(document).ready(function() {
	var timer_status = reverse('time_tracking', function(url) {
        var request_url = url + "/?timer_status";
        $.ajax({
            url: request_url,
            success: function(data) {
                if (data == '1') {
                    $('.timer_option').css('color', '#e74c3c');
                }
            }
        })
    })
});