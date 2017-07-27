
/**
 * Sort a table based on the column clicked
 * Source: https://www.w3schools.com/howto/howto_js_sort_table.asp
 */
function sortTable(n, tableId) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById(tableId);
    switching = true;
    // Set the sorting direction to ascending:
    dir = "asc";
    // Make a loop that will continue until
    // no switching has been done:
    while (switching) {
        //start by saying: no switching is done:
        switching = false;
        rows = table.getElementsByTagName("TR");
        // Loop through all table rows (except the
        // first, which contains table headers):
        for (i = 1; i < (rows.length - 1); i++) {
            //start by saying there should be no switching:
            shouldSwitch = false;
            // Get the two elements you want to compare,
            // one from current row and one from the next:
            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];
            //check if the two rows should switch place,
            // based on the direction, asc or desc:
            if (dir === "asc") {
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    // if so, mark as a switch and break the loop:
                    shouldSwitch = true;
                    break;
                }
            } else if (dir === "desc") {
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                    // if so, mark as a switch and break the loop:
                    shouldSwitch = true;
                    break;
                }
            }
        }
        if (shouldSwitch) {
            // If a switch has been marked, make the switch
            // and mark that a switch has been done:
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            // Each time a switch is done, increase this count by 1:
            switchcount++;
        } else {
            // If no switching has been done AND the direction is "asc",
            // set the direction to "desc" and run the while loop again.
            if (switchcount === 0 && dir === "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}

/**
 * Show the create project modal, used to register a click event on the relevant button
 */
function addProjectModal() {
    $('#createProjectModal').modal('show');
}

/**
 * Ajax function to add a project
 * If there is an error with validation, we will put the relevant message next to the field where the error occurred
 * If the project is successfully created, the webpage body will be replaced
 *
 * An unknown error (non-success from server) will create an alert
 */
function addProjectAjax() {
    var frm = $(document).find('#createProjectForm');
    clearFormErrors(frm);
    $.ajax({
        type: frm.attr('method'),
        url: frm.attr('action'),
        data: frm.serialize(),
        success: function (data) {
            try {
                var resp = jQuery.parseJSON(data);
                for (var key in resp) {
                    $('#error_' + key).html(resp[key][0].message);
                }
            }
            catch (err) {
                replaceBody(data);
            }
        },
        error: function (data) {
            alert('Something went wrong!');
        }
    });
}

/**
 * Show the delete project modal, used to register a click event on the relevant button
 * @param e button clicked, we get the pid from a substring of the button's id
 */
function deleteProjectModal(e) {
    var pid = $(this).attr('id').substring(7);
    $('#projectDeleteId').html(pid);
    $('#deleteProjectModal').modal('show');
    $('#deleteProjectField').attr('value', pid);
}

/**
 * Ajax function to delete a project
 * Successful responses will replace the body of the current list
 *
 * Unknown errors will create an alert box
 */
function deleteProjectAjax() {
    var frm = $(document).find('#deleteProjectForm');
    $.ajax({
        type: frm.attr('method'),
        url: frm.attr('action'),
        data: frm.serialize(),
        success: function (data) {
            replaceBody(data);
        },
        error: function (data) {
            alert('Something went wrong!');
        }
    });
}

/**
 * Reset the create project form, used to register a click event on the relevant button
 */
function resetAndClearCreateForm() {
    resetAndClearForm($('#createProjectForm'));
}

/**
 * Reset the form, clearing out any data entered
 * @param form The form that we are clearing the data from
 */
function resetForm(form) {
    form[0].reset();
}

/**
 * Clear errors for the provided form. Errors are defined by the presence of the class "form-error"
 * @param form The form that we are clearing errors from
 */
function clearFormErrors(form) {
    form.find($('.form-error')).html("")
}

/**
 * Reset a form and clear any errors
 * @param form The form that we are clearing errors from
 */
function resetAndClearForm(form) {
    resetForm(form);
    clearFormErrors(form);
}

/**
 * Replace the body of the current document with the body contained within the input.
 * To make sure events do not fire more than once, we have to make sure to remove the 'click' events that we added before
 * @param html String containing a <body></body> element to replace with
 */
function replaceBody(html) {
    // We have to make sure to remove the old click listeners so that we do not get multiple submits
    $('.add-project').off('click', addProjectModal);
    $('#resetFormButton').off('click', resetAndClearCreateForm);
    $('.delete-project').off('click', deleteProjectModal);
    $(document).off('click', '#createProjectButton', addProjectAjax);
    $(document).off('click', '#deleteProjectButton', deleteProjectAjax);

    // Replace the old body with the new body
    $('body').empty().html( html.substring(html.indexOf("<body>")+6, html.indexOf("</body>")) );
    onReady();
}

/**
 * Initialization function to be called every time we have loaded the page/new body
 */
function onReady() {
    $('[data-toggle="tooltip"]').tooltip();
    $('.add-project').on('click', addProjectModal);
    $('#resetFormButton').on('click', resetAndClearCreateForm);
    $('.delete-project').on('click', deleteProjectModal);

    $(document).on('click', '#createProjectButton', addProjectAjax);
    $(document).on('click', '#deleteProjectButton', deleteProjectAjax);
}

/**
 * Make sure everything is properly initialized once the document is ready
 */
$(document).ready(function () {
    onReady();
    $(document).on('hidden.bs.modal', function () {clearFormErrors($(this).find('form'))} );
});