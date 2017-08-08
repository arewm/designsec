/**
 * Make the first letter of a string capitalized
 * @returns {string}
 */
String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
};

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
 * Enable the tinymce editor on an arbitrary element(s)
 * @param selector The css selector matching the element(s) to enable the editor for
 */
function enableMCE(selector) {
    console.log(selector);
    // convert all desired textareas to use tinymce WYSIWYG editor
    tinymce.init({
        selector: selector,
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
}

/**
 * Get a model corresponding to the corresponding element. The function returned uses several HTML-5 attributes:
 * data-model-operation: The operation to be performed by the modal
 * data-target: The django model target for the operation
 * data-id: The django model id of the target to be operated on. This is not needed for all operations (i.e. add)
 * @returns {Function}
 */
function getModal(modalContainer){
    return function () {
        var modalType = $(this).attr('data-modal-operation');
        var target = $(this).attr('data-target');
        var targetId = $(this).attr('data-id');
        var formId = '#' + modalType + 'ModalMaker';
        var deleteModalMaker = $(formId);
        deleteModalMaker.find('input[name=id]').val(targetId);
        deleteModalMaker.find('input[name=target]').val(target);
        $.ajax({
            type: deleteModalMaker.attr('method'),
            url: deleteModalMaker.attr('action'),
            data: deleteModalMaker.serialize(),
            success: function (resp) {
                // console.log(resp);
                // console.log(resp.modal_id);
                // console.log($(resp.modal_id));
                // console.log($(resp.modal_id)===null);
                // remove all prior tinymce editors. We will re-enable it for any new modal we create
                tinymce.remove();
                // de-register click events and remove previous modals
                modalContainer.find(resp.modal_id).each(function () {
                    $(this).find(resp.form_button).each(function () {$(this).off('click')});
                    $(this).remove();
                });
                modalContainer.append(resp.modal);
                var modal = $(resp.modal_id);

                $(resp.form_button).on('click', callModalAjax(resp.form_id));
                // show tooltips
                modal.find('[data-toggle="tooltip"]').tooltip({
                    trigger : 'hover'
                });
                // Enable the mce editor if we need to
                var mceTexts = [];
                $(resp.form_id).find('textarea').each(function() {
                    if (!$(this).prop('readonly')) {
                        mceTexts.push(resp.form_id + ' #' + $(this).attr('id'));
                    }
                });
                if (mceTexts.length) {
                    // We have some non-readonly texts
                    enableMCE(mceTexts.join());
                }
                $('#reset' + modalType.capitalize() + target.capitalize() + 'FormButton').on('click', resetAndClearCreateForm);
                modal.modal('show');
            },
            error: function () {
                alert('Something went wrong!')
            }
        });
    }
}

/**
 * Ajax function to submit a form contained a modal. If there are validation errors, they will be displayed on the form.
 * Successful responses will reload the window
 *
 * Unknown errors will create an alert box
 */
function callModalAjax(formId) {
    var frm = $(document).find(formId);
    return function () {
        frm.find('textarea').each(function () {
            var c = tinyMCE.get($(this).attr('id'));
            if (c !== null) {
                console.log(c);
                console.log($(this).attr('id'));
                $(this).html(c.getContent());
            }
        });
        clearFormErrors(frm);
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function () {
                location.reload()
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
}