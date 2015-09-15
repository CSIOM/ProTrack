$(document).ready(function() {
    $(".class_project").hide();
    $('#id_view').change(function(){
    view_id = $('#id_view').val();
    if(view_id == 2){
         $('.class_project').show();
         $('.class_project').show();
        }
    else{
        $('.class_project').hide();
        $('.class_project').hide();
    }
    });
    
});
