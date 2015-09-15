$(document).on("click", '.view-history', function(event) {
        var project = this.id;
        var a = reverse('view_history', function(url) {
            var request_url = url + "/?project=" + project;
            $.ajax({
                url: request_url,
                success: function(data){

                    BootstrapDialog.show({
                        size: BootstrapDialog.SIZE_WIDE,
                        title: '<b>History</b>',
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