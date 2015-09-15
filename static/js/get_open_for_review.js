$(document).ready(function(){
    $('#id_review_date').change(function(){
        $('#open-for-review').empty();
        date = $('#id_review_date').val();
        var a = reverse('review', function(url) {
        var name = $('#id_name').val();
        if(name){
            var request_url = url + "/?date=" + date + '&name=' + name;
        }
        else{
            var request_url = url + "/?date=" + date;
        }
        $.ajax({
            url: request_url,
            success: function(data){
                 $("#open-for-review").append(data);
                }
            })
        })
    })
    $('#id_name').on("change", function(){
        $('#open-for-review').empty();
        name = $('#id_name').val();
        var a = reverse('review', function(url) {
        date = $('#id_review_date').val();
        if(date){
            var request_url = url + "/?date=" + date + '&name=' + name;
        }
        else{
            var request_url = url + "/?name=" + name;
        }
        $.ajax({
            url: request_url,
            success: function(data){
                 $("#open-for-review").append(data).show('slow');
                }
            })
        })
    })
});