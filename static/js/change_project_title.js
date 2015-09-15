$(document).on("click", '.change-project-title', function(event) {
        var project = this.id;
        var a = reverse('change_project_title', function(url) {
            var request_url = url + "/?project=" + project;
            $.ajax({
                url: request_url,
                success: function(data){

                    BootstrapDialog.show({
                        title: '<b>Project Title</b>',
                        message: data,

                        buttons: [{
                            icon: 'glyphicon glyphicon-ok',
                            cssClass: 'btn btn-success',
                            label: ' Change Title',
                            action: function(dialogItself){
                              var project_title = $('#id_project_title').val();
                              var error = 0;
                              if(project_title == ''){
                                error=1;
                              }
                              if( error == 1){
                                $('#warning').show();
                              }
                                else{
                                    var a = reverse('change_project_title', function(url) {
                                    var request_url = url + "/?project=" + project + "&project_title=" + project_title;
                                    $.ajax({
                                        url: request_url,
                                        success: function(data){
                                          location.reload();
                                        dialogItself.close();
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