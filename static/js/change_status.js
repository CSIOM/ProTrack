$(document).on("click", '.change-status', function(event) {
        var project = this.id;
        var a = reverse('change_status', function(url) {
            var request_url = url + "/?project=" + project;
            $.ajax({
                url: request_url,
                success: function(data){

                    BootstrapDialog.show({
                        title: '<b>Project Status</b>',
                        message: data,

                        buttons: [{
                            icon: 'glyphicon glyphicon-ok',
                            cssClass: 'btn btn-success',
                            label: ' Change Status',
                            action: function(dialogItself){
                              var status = $('#id_status').val();
                              var remarks = $('#remarks').val();
                              var error = 0;
                              if(status == ''){
                                error=1;
                              }

                              if (remarks == '')
                              {
                                error = 1;
                              }

                              if( error == 1){
                                $('#warning').show();
                              }
                                else{
                                    var a = reverse('change_status', function(url) {
                                    var request_url = url + "/?project=" + project + "&status=" + status + "&remarks=" + remarks;
                                    $.ajax({
                                        url: request_url,
                                        success: function(data){
                                        dialogItself.close();
                                        $('#status').text(data);
                                    }
                                })
                                })
                              }
                            }
                        },
                            {
                            icon: 'glyphicon glyphicon-ok',
                            cssClass: 'btn btn-danger',
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