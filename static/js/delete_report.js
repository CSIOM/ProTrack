$(document).on("click", '.delete-report', function(event) {
        var report_id = this.id;
        BootstrapDialog.show({
            title: '<b>Delete Report?</b>',
            message: "Are you sure that you want to remove this report?",

            buttons: [{
                icon: 'glyphicon glyphicon-ok',
                cssClass: 'btn btn-success',
                label: ' Yes',
                action: function(dialogItself){
                    dialogItself.close();
                    var a = reverse('delete_report', function(url) {
                        var request_url = url + "/?report_id=" + report_id;
                        $.ajax({
                            url: request_url,
                            success: function(data) {
                                $("." + report_id).hide(1000, function() {
                                    $("." + report_id).remove();
                                });
                            }
                        })
                    })
                }
            },
            {
                icon: 'glyphicon glyphicon-remove',
                cssClass: 'btn btn-danger',
                label: ' No',
                action: function(dialogItself){
                    dialogItself.close();
                }
            }]
        });
});