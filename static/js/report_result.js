$(document).ready(function(){
    $('#id_view').change(function(){
        $('#reportdatadiv').empty();
        view_val = $('#id_view').val();
        if(view_val == 1){
            var a = reverse('view_report', function(url) {
            var request_url = url + "/?view_val=" + view_val;
            $.ajax({
                url: request_url,
                success: function(data){
                    var div = document.getElementById('reportdatadiv');
                    div.innerHTML = div.innerHTML + data;
                }
            })
        })
    }
    })
    $('#id_project').change(function(){
        $('#reportdatadiv').empty();
        view_val = $('#id_view').val();
        project_val = $('#id_project').val();
        if(view_val == 2){
            var a = reverse('view_report', function(url) {
            var request_url = url + "/?view_val=" + view_val + "&project_val=" + project_val;
            $.ajax({
                url: request_url,
                success: function(data){
                    var div = document.getElementById('reportdatadiv');
                    div.innerHTML = div.innerHTML + data;
                }
            })
        })
        }
    })
});