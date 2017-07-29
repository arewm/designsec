/**
 * Function to remove all attributes from a jQuery object
 * @returns {*}
 */
jQuery.fn.removeAttributes = function () {
    return this.each(function () {
        var attributes = $.map(this.attributes, function (item) {
            return item.name;
        });
        var img = $(this);
        $.each(attributes, function (i, item) {
            img.removeAttr(item);
        });
    });
};

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
    frm.find('textarea').each(function () {
        $(this).html(tinyMCE.get($(this).attr('id')).getContent());
    });
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
        error: function () {
            alert('Something went wrong!');
        }
    });
}

/**
 * Show the delete project modal, used to register a click event on the relevant button
 */
function deleteProjectModal() {
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
        error: function () {
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
    $('#resetCreateProjectFormButton').off('click', resetAndClearCreateForm);
    $('.delete-project').off('click', deleteProjectModal);
    $(document).off('click', '#createProjectButton', addProjectAjax);
    $(document).off('click', '#deleteProjectButton', deleteProjectAjax);

    // Replace the old body with the new body
    $('body').empty().removeAttributes().html(html.substring(html.indexOf("<body>") + 6, html.indexOf("</body>")));
    tinymce.remove();
    onReady();
}

/**
 * Initialization function to be called every time we have loaded the page/new body
 */
function onReady() {
    // show tooltips
    $('[data-toggle="tooltip"]').tooltip();
    // enable modals
    $('.add-project').on('click', addProjectModal);
    $('#resetCreateProjectFormButton').on('click', resetAndClearCreateForm);
    $('.delete-project').on('click', deleteProjectModal);
    // register Ajax functions
    $(document).on('click', '#createProjectButton', addProjectAjax);
    $(document).on('click', '#deleteProjectButton', deleteProjectAjax);
    // Convert the adminTable to a DataTable object
    var table = $('#adminTable').DataTable({
        paging: true,
        scrollCollapse: true,
        fixedHeader: {
            header: true,
            footer: true
        }
    });
    // allow the table to resize with the window
    table.table().node().style.width = null;
    // convert all textareas to use tinymce WYSIWYG editor
    tinymce.init({
        selector: 'textarea',
        branding: false,
        format: 'html',
        height: 500,
        menubar: false,
        plugins: [
            'advlist autolink lists link visualblocks code table contextmenu paste code'
        ],
        advlist_bullet_styles: 'default,circle,square',
        advlist_number_styles: 'default,lower-alpha,upper-alpha,lower-roman,upper-roman',
        paste_data_images: false,
        toolbar: 'styleselect | bold italic | alignleft aligncenter alignright | table ' +
                 '| bullist numlist outdent indent | link | code',
        content_css: [
            '//fonts.googleapis.com/css?family=Lato:300,300i,400,400i',
            '//www.tinymce.com/css/codepen.min.css']
    });
}

/**
 * Make sure everything is properly initialized once the document is ready
 */
$(document).ready(function () {
    onReady();
    $(document).on('hidden.bs.modal', function () {
        clearFormErrors($(this).find('form'))
    });
});