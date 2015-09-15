$(document).ready(function(){

    report_type = $("input[name=report_type]:checked").val()
    if(report_type){
        if(report_type==1){
            member_id = $('#members-report').val();
            $('#members-report').empty();
            project_id = $('#report-project').val();
            reverse('src.main.views.members', function(url) {
                var request_url = url + "/?project_id=" + project_id;
                $.ajax({
                    url: request_url,
                    datatype:'json',
                    success: function(data){
                        
                        $.each(JSON.parse(data), function(key, value){
                           $('#members-report').append('<option value="' + key.split('_')[1] + '">' + value +'</option>').innerHTML;
                           $("#members-report").val(member_id);
                       });
                    }
                })
            });
        }
        if(report_type==2){
            $('#members-report').hide();
            $("label[for='members-report']").hide();
        }
        if(report_type==3){
            $('#report-project').hide();
            $("label[for='report-project']").hide();
        }
    }
    else{
        $('#members-report').hide();
        $("label[for='members-report']").hide();
    }
    
    $("input[type='radio']").click(function(){
        report_type = $("input[name=report_type]:checked").val()
        if(report_type==1){
            $('#members-report').empty();
            $('#members-report').show();
            $("label[for='members-report']").show();
            $('#report-project').show();
            $("label[for='report-project']").show();
        }
        if(report_type==2){
            $('#members-report').hide();
            $("label[for='members-report']").hide();
            $('#report-project').show();
            $("label[for='report-project']").show();
        }
        if(report_type==3){
            $('#members-report').empty();
            $('#members-report').show();
            $("label[for='members-report']").show();
            $('#report-project').hide();
            $("label[for='report-project']").hide();
            reverse('src.main.views.members', function(url) {
                var request_url = url;
                $.ajax({
                    url: request_url,
                    datatype:'json',
                    success: function(data){
                        $.each(JSON.parse(data), function(key, value){
                         $('#members-report').append('<option value="' + key.split('_')[1] + '">' + value +'</option>').innerHTML;

                     });
                    }
                })
            });
        }
    })
$("#report-project").click(function(){
    $('#members-report').empty();
    report_type = $("input[name=report_type]:checked").val()
    if (report_type==1){
        project_id = $(this).val();
        reverse('src.main.views.members', function(url) {
            var request_url = url + "/?project_id=" + project_id;
            $.ajax({
                url: request_url,
                datatype:'json',
                success: function(data){
                    $.each(JSON.parse(data), function(key, value){
                     $('#members-report').append('<option value="' + key.split('_')[1] + '">' + value +'</option>').innerHTML;
                 });
                }
            })
        });
    }
})
});

