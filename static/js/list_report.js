$(document).ready(function(){
    function get_values(){
        start_date = $('#id_start_date').val();
        end_date = $('#id_end_date').val();
        var a = reverse('view_report', function(url) {
        var request_url = url + "/?list_report&start_date=" + start_date + '&end_date=' + end_date;
        $.ajax({
            url: request_url,
            success: function(data){
                $('#list-report-display').empty();
                 $("#list-report-display").append(data).show('slow');
                }
            })
        })
    }
    if ($('#id_start_date').val()){
        get_values();
    }
    $('#id_start_date').change(function(){
        get_values();
    })
    $('#id_end_date').on("change", function(){
        start_date = $('#id_start_date').val();
        end_date = $('#id_end_date').val();
        var a = reverse('view_report', function(url) {
        var request_url = url + "/?list_report&start_date=" + start_date + '&end_date=' + end_date;
        $.ajax({
            url: request_url,
            success: function(data){
                $('#list-report-display').empty();
                 $("#list-report-display").append(data).show('slow');
                }
            })
        })
    })
});