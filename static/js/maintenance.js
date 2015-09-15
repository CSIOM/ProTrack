$(document).ready(function(){
	var a = reverse('maintainer', function(url) {
            var request_url = url
            $.ajax({
                url: request_url,
                success: function(data){
                    if (data != 3){
                    	var maintenance_url =   reverse('maintenance', function(url) {
                window.location.href = url;
    })
                    }
                }
            })
        })

});
