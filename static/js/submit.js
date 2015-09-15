$(document).ready(function(){
            $('#comment').click(function(){
                        $('#report_id').attr("type","text");                
})
    var frm = $('#comment-form');
    frm.submit(function () {
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function (data) {
                location.reload()
                $('#id_comment').val("");
            }
        });
        return false;
    });
});