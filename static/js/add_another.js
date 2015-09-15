$(document).ready(function() {
    $("#add_another").click(function() {
        var table = document.getElementById("myTable");
        var tablerow = table.insertRow(-1);
        var cell0 = tablerow.insertCell(0);
        cell0.appendChild($("#id_self_rating").parent("td").clone()[0]);

        var cell1 = tablerow.insertCell(1);
        cell1.appendChild($("#id_duration_in_hours").parent("td").clone()[0]);
        $('.class_duration_in_hours').timepicker({
            defaultTime: 'value',
            minuteStep: 1,
            disableFocus: true,
            template: 'dropdown',
            showMeridian:false
        });

        var cell2 = tablerow.insertCell(2);
        cell2.appendChild($("#id_work_done").parent("td").clone()[0]);

        var cell3 = tablerow.insertCell(3);
        cell3.appendChild($("#id_struggle").parent("td").clone()[0]);

        var cell4 = tablerow.insertCell(4);
        cell4.appendChild($("#id_tags").parent("td").clone()[0]);
    });
    $("#delete_row").click(function() {
        var rowCount = $('#myTable tr').length;
        if(rowCount > 2){
         row = document.getElementById('myTable').deleteRow(-1);
        }
    });
});
