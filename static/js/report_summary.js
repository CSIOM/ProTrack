$(document).on("click", '.report_summary', function(event) {
        var addressValue = $(this).attr("href");
        var a = reverse('view_report', function(url) {
            var request_url = url + "/?" + addressValue;
            $.ajax({
                url: request_url,
                success: function(data){

                    BootstrapDialog.show({
                        size: BootstrapDialog.SIZE_WIDE,
                        title: '<b>Report Summary</b>',
                        message: data,

                        buttons: [{
                            icon: 'glyphicon glyphicon-ok',
                            cssClass: 'btn btn-success',
                            label: ' Close',
                            action: function(dialogItself){
                                dialogItself.close();
                            }
                        }]
                    })
                }
            })
        });
        return false;
});