
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
    $('#adminTable').DataTable();
}

/**
 * Make sure everything is properly initialized once the document is ready
 */
$(document).ready(function () {
    onReady();
    $(document).on('hidden.bs.modal', function () {clearFormErrors($(this).find('form'))} );
});