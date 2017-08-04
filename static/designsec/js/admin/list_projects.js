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
    $('#addProjectModal').modal('show');
}

/**
 * Ajax function to add a project
 * If there is an error with validation, we will put the relevant message next to the field where the error occurred
 * If the project is successfully created, the page will be reloaded
 *
 * An unknown error (non-success from server) will create an alert
 */
function addProjectAjax() {
    var frm = $(document).find('#addProjectForm');
    frm.find('textarea').each(function () {
        $(this).html(tinyMCE.get($(this).attr('id')).getContent());
    });
    clearFormErrors(frm);
    $.ajax({
        type: frm.attr('method'),
        url: frm.attr('action'),
        data: frm.serialize(),
        success: function () {
            location.reload();
        },
        error: function (jqXHR) {
            if (jqXHR.status === 400) {
                var resp = JSON.parse(jqXHR.responseJSON);
                $.each(resp, function (k, v) {
                    $('#error_' + k).html(v[0].message);
                });
            }
            else {
                alert('Something went wrong!')
            }
        }
    });
}

/**
 * Get the delete project modal, show it, and register the submit click
 */
var lastDeleteProjectModal = null;
function deleteProjectModal() {
    var projId = $(this).attr('id').substring(7);
    // deleteModalMaker = $('#deleteModalMaker');
    // deleteModalMaker.find('input[name=id]').val(projId);
    // deleteModalMaker.find('input[name=target]').val('project');
    // $.ajax({
    //     type: deleteModalMaker.attr('method'),
    //     url: deleteModalMaker.attr('action'),
    //     data: deleteModalMaker.serialize(),
    //     success: function (resp) {
    //         console.log(resp);
    //         if (lastModal !== null) {
    //             $(resp.form_button).off('click');
    //             lastModal.remove()
    //         }
    //         $('body').append(resp.modal);
    //         var modal = $(resp.modal_id);
    //
    //         $(resp.form_button).on('click', deleteProjectAjax(resp.form_id));
    //         modal.modal('show');
    //         lastModal = modal;
    //     },
    //     error: function() {
    //         alert('Something went wrong!')
    //     }
    // });
    getModal(projId, '#deleteModalMaker', 'project', lastDeleteProjectModal)
}

var lastEditContactModal = null;
function editContactModal(){
    var projectId = $(this).attr('id').substring(5);
    getModal(projectId, '#editModalMaker', 'contact', lastEditContactModal)
}

function getModal(projectId, formId, target, lastModal){
    deleteModalMaker = $(formId);
    deleteModalMaker.find('input[name=id]').val(projectId);
    deleteModalMaker.find('input[name=target]').val(target);
    $.ajax({
        type: deleteModalMaker.attr('method'),
        url: deleteModalMaker.attr('action'),
        data: deleteModalMaker.serialize(),
        success: function (resp) {
            console.log(resp);
            if (lastModal !== null) {
                $(resp.form_button).off('click');
                lastModal.remove()
            }
            $('body').append(resp.modal);
            var modal = $(resp.modal_id);

            $(resp.form_button).on('click', deleteProjectAjax(resp.form_id));
            modal.modal('show');
            lastModal = modal;
        },
        error: function() {
            alert('Something went wrong!')
        }
    });
}

/**
 * Ajax function to delete a project
 * Successful responses will reload the window
 *
 * Unknown errors will create an alert box
 */
function deleteProjectAjax(formId) {
    var frm = $(document).find(formId);
    return function () {
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function () {
                location.reload()
            },
            error: function (jqXHR) {
                if (jqXHR.status === 400) {
                    alert(jqXHR.responseJSON.reason);
                }
                else {
                    alert('Something went wrong!')
                }
            }
        });
    }
}

/**
 * Reset the create project form, used to register a click event on the relevant button
 */
function resetAndClearCreateForm() {
    resetAndClearForm($('#addProjectForm'));
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
 * Function to allow additional values in a multi-select box to be created. Clearly not implemented yet.
 */
function makeSelectAdd() {
    $('.check-select').find('select').each(function () {
        console.log($(this).attr('name'))
    })
}

/**
 * Make sure everything is properly initialized once the document is ready
 */
$(document).ready(function () {
    // show tooltips
    $('[data-toggle="tooltip"]').tooltip({
        trigger : 'hover'
    });
    // enable modals
    $('.add-project').on('click', addProjectModal);
    $('#resetAddProjectFormButton').on('click', resetAndClearCreateForm);
    $('.delete-project').on('click', deleteProjectModal);
    $('.edit-contact').on('click', editContactModal);
    // register Ajax functions
    $(document).on('click', '#addProjectButton', addProjectAjax);
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
        toolbar: 'styleselect | bold italic | alignleft aligncenter ' +
                 '| bullist numlist | outdent indent | link table | code',
        content_css: [
            '//fonts.googleapis.com/css?family=Lato:300,300i,400,400i',
            '//www.tinymce.com/css/codepen.min.css']
    });
    $(document).on('hidden.bs.modal', function () {
        clearFormErrors($(this).find('form'))
    });
});