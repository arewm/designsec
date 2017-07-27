
function sortTable(n, tableId) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById(tableId);
    switching = true;
    //Set the sorting direction to ascending:
    dir = "asc";
    /*Make a loop that will continue until
     no switching has been done:*/
    while (switching) {
        //start by saying: no switching is done:
        switching = false;
        rows = table.getElementsByTagName("TR");
        /*Loop through all table rows (except the
         first, which contains table headers):*/
        for (i = 1; i < (rows.length - 1); i++) {
            //start by saying there should be no switching:
            shouldSwitch = false;
            /*Get the two elements you want to compare,
             one from current row and one from the next:*/
            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];
            /*check if the two rows should switch place,
             based on the direction, asc or desc:*/
            if (dir === "asc") {
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    //if so, mark as a switch and break the loop:
                    shouldSwitch = true;
                    break;
                }
            } else if (dir === "desc") {
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                    //if so, mark as a switch and break the loop:
                    shouldSwitch = true;
                    break;
                }
            }
        }
        if (shouldSwitch) {
            /*If a switch has been marked, make the switch
             and mark that a switch has been done:*/
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            //Each time a switch is done, increase this count by 1:
            switchcount++;
        } else {
            /*If no switching has been done AND the direction is "asc",
             set the direction to "desc" and run the while loop again.*/
            if (switchcount === 0 && dir === "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}

function resetForm(form) {
    form[0].reset();
}
function clearFormErrors(form) {
    form.find($('.form-error')).html("")
}
function resetAndClearForm(form) {
    resetForm(form);
    clearFormErrors(form);
}
function initialLoad() {
    $('.add-project').on('click', function(e) {
        $('#createProjectModal').modal('show');
    });
    $('#resetFormButton').on('click', function(e) {
        resetAndClearForm($('#createProjectForm'));
    });
    $('[data-toggle="tooltip"]').tooltip();

    $(document).on('click', '#createProjectButton', function () {
        var frm = $(document).find('#createProjectForm');
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function (data) {
                try {
                    var resp = jQuery.parseJSON(data);
                    //console.log(data)
                    for (var key in resp) {
                        //console.log(resp[key][0].message)
                        //r = jQuery.parseJSON(resp[key][0]);
                        //console.log(r.message);
                        $('#error_' + key).html(resp[key][0].message);
                    }
                }
                catch (err) {
                    var body = data.substring(data.indexOf("<body>")+6,data.indexOf("</body>"));
                    $('body').html(body);
                    initialLoad();
                }
            },
            error: function (data) {
                alert('Something went wrong!');
            }
        });
    });
    $(document).on('hidden.bs.modal', function () {
        clearFormErrors($(this).find('form'));
    });

}

$(document).ready(function () {
    initialLoad();
});