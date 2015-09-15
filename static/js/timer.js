$(document).ready(function() {
    var time_var1;
    var time_var2;
    var timer_start_click = 0;

    $('#reset-button').click(function() {
        var a = reverse('time_tracking', function(url) {
            var request_url = url + "/?reset";
            $.ajax({
                url: request_url,
                success: function(data) {
                    window.location.href = url
                }
            })
        })
    });
    var timer_status = reverse('time_tracking', function(url) {
        var request_url = url + "/?timer_status";
        $.ajax({
            url: request_url,
            success: function(data) {
                if (data == '1') {
                    $('.timer_option').css('color', '#e74c3c');
                    timer_status = $('#timer-status').text();
                    if (timer_status == '1') {
                        timer_paused = $('#timer-paused').text();
                        if (timer_paused == '0') {

                            time_var1 = setInterval(function timer() {
                                var timer = $("#hours-value").text().split(':');
                                var new_timer_sec = format_num(Math.floor(timer[2]) + Math.floor(1));
                                if (new_timer_sec > 59) {
                                    var new_timer_sec = format_num(0);
                                    var new_time = increment_timer($("#hours-value").text());
                                    $("#hours-value").text(new_time);
                                    return true;
                                }
                                var new_time = timer[0] + ':' + timer[1] + ':' + new_timer_sec;
                                $("#hours-value").text(new_time);
                                return true;
                            }, 1000);
                        }
                    } else {
                        var timer = reverse('time_tracking', function(url) {
                            var request_url = url + "/?get_time";
                            $.ajax({
                                url: request_url,
                                success: function(data) {
                                    var window_url = String(window.location);
                                    var url_split = window_url.split('/');
                                    if (url_split[3] != 'edit_report') {
                                        $('#id_duration_in_hours').val(data);
                                    }
                                }
                            })
                        })
                        var a = reverse('time_tracking', function(url) {
                            var request_url = url + "/?get_work_done";
                            $.ajax({
                                url: request_url,
                                success: function(data) {
                                    $('#id_work_done').val(data);
                                }
                            })
                        })
                        $('.time_tracker_report_form').show();
                    }
                }
            }
        })
    })

    function format_num(num) {
        return (num < 10) ? '0' + num.toString() : num.toString();
    }

    function increment_timer(time) {
        var current_time = time.split(':');
        var current_mins = Math.floor(current_time[0] * 60) + Math.floor(current_time[1]);
        var updated_mins = current_mins + 1;
        var updated_time_hours = format_num(Math.floor(updated_mins / 60));
        var updated_time_mins = format_num(updated_mins % 60);

        return (updated_time_hours + ':' + updated_time_mins + ':' + '00');
    }

    function show_hide_form(timer_status) {
        if (timer_status == '0') {
            $("#timer-status").text('1');
            time_var2 = setInterval(function timer() {
                var timer = $("#hours-value").text().split(':');
                var new_timer_sec = format_num(Math.floor(timer[2]) + Math.floor(1));
                if (new_timer_sec > 59) {
                    var new_timer_sec = format_num(0);
                    var new_time = increment_timer($("#hours-value").text());
                    $("#hours-value").text(new_time);
                    return true;
                }
                var new_time = timer[0] + ':' + timer[1] + ':' + new_timer_sec;
                $("#hours-value").text(new_time);
                return true;
            }, 1000);
        } else if (timer_status == '1') {
            $('.timer').hide();
            var dt = new Date($.now());
            var time = dt.getHours() + ":" + dt.getMinutes();
            $("#id_time").val(time);
            var a = reverse('time_tracking', function(url) {
                var request_url = url + "/?get_work_done";
                $.ajax({
                    url: request_url,
                    success: function(data) {
                        $('#id_work_done').val(data);
                    }
                })
            })
            $('.time_tracker_report_form').show();
            var timer = $("#hours-value").text().split(':');
            var current_time = timer[0] + ':' + timer[1];
            $('#id_duration_in_hours').val(current_time);

        }
    }

    function change_values() {
        $('#pause-button').show();
        $('.timer_option').css('color', '#e74c3c');
        $('#timer-button').removeClass("btn-success");
        $('#timer-button').addClass("btn-danger");
        $('#button-label').text('Stop Timer');
        timer_status = $('#timer-status').text();
        show_hide_form(timer_status);
    }

    function handel_timer() {
        var timer_status = reverse('time_tracking', function(url) {
            var request_url = url + "/?timer_status";
            $.ajax({
                url: request_url,
                success: function(data) {
                    if (data == '0') {
                        BootstrapDialog.show({
                            title: '<b>Description of Task</b>',
                            message: '<textarea class="form-control" cols="20" id="work_done" rows="3">',

                            buttons: [{
                                icon: 'glyphicon glyphicon-ok',
                                cssClass: 'btn btn-success',
                                label: ' Save',
                                action: function(dialogItself) {
                                    timer_start_click = 1;
                                    var work_done = $("#work_done").val();
                                    var a = reverse('time_tracking', function(url) {
                                        var request_url = url + "/?start_stop_time&work=" + work_done;
                                        $.ajax({
                                            url: request_url,
                                            success: function(data) {
                                                dialogItself.close();
                                                change_values();
                                                var a = reverse('time_tracking', function(url) {
                                                    window.location.href = url;
                                                })
                                            }
                                        })
                                    })
                                }
                            }, {
                                icon: 'glyphicon glyphicon-remove',
                                cssClass: 'btn btn-info',
                                label: ' Ask Me Later',
                                action: function(dialogItself) {
                                    timer_start_click = 1;
                                    var a = reverse('time_tracking', function(url) {
                                        var request_url = url + "/?start_stop_time";
                                        $.ajax({
                                            url: request_url,
                                            success: function(data) {
                                                dialogItself.close();
                                                change_values();
                                                var a = reverse('time_tracking', function(url) {
                                                    window.location.href = url;
                                                })
                                            }
                                        })
                                    })
                                }
                            }, {
                                icon: 'glyphicon glyphicon-remove',
                                cssClass: 'btn btn-danger',
                                label: ' Cancel',
                                action: function(dialogItself) {
                                    dialogItself.close();
                                }
                            }]

                        })
                    } else {
                        var a = reverse('time_tracking', function(url) {
                            var request_url = url + "/?start_stop_time";
                            $.ajax({
                                url: request_url,
                                success: function(data) {
                                    timer_status = $('#timer-status').text();
                                    show_hide_form(timer_status);
                                }
                            })
                        })
                    }
                }

            })
        })
    }

    $('#timer-button').click(function() {

        handel_timer();
    });

    $('#pause-button, #timer-button-pause').click(function() {
        var a = reverse('time_tracking', function(url) {
            var request_url = url + "/?pause";
            $.ajax({
                url: request_url,
                success: function(data) {}
            })
        })
        timer_paused = $('#timer-paused').text();
        if (timer_paused == '0') {
            clearInterval(time_var1);
            clearInterval(time_var2);
            $('#pause-button-icon').removeClass("glyphicon-pause");
            $('#pause-button-icon').addClass("glyphicon-play");
            $('#pause-button-label').text('Resume Timer');
            $('#timer-paused').text('1');
        } else if (timer_paused == '1') {
            $('#pause-button-icon').removeClass("glyphicon-play");
            $('#pause-button-icon').addClass("glyphicon-pause");
            $('#pause-button-label').text('Pause Timer');
            $('#timer-paused').text('0');
            time_var2 = setInterval(function timer() {
                var timer = $("#hours-value").text().split(':');
                var new_timer_sec = format_num(Math.floor(timer[2]) + Math.floor(1));
                if (new_timer_sec > 59) {
                    var new_timer_sec = format_num(0);
                    var new_time = increment_timer($("#hours-value").text());
                    $("#hours-value").text(new_time);
                    return true;
                }
                var new_time = timer[0] + ':' + timer[1] + ':' + new_timer_sec;
                $("#hours-value").text(new_time);
                return true;
            }, 1000);
        }
    })

    $('#timer-button-right').click(function() {

        handel_timer();
    })

});