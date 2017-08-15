/**
 * Make the first letter of a string capitalized
 * @returns {string}
 */
String.prototype.capitalize = function () {
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
 * Get a modal corresponding to the corresponding element. The function returned uses several HTML-5 attributes:
 * data-modal-operation: The operation to be performed by the modal
 * data-target: The django model target for the operation
 * data-id: The django model id of the target to be operated on. This is not needed for all operations (i.e. add)
 *
 * @param modalContainer The jQuery element containing the container for the modal HTML to be put
 * @param {boolean} removeMceEditors The action to trigger first when we successfully get a modal
 * @param {string} modalMakerIdPart the end of the ID for the form to use to generate the modal
 * @param {function} [ajaxSuccessFunction] The function to call on a successful AJAX for the retrieved modal's action
 * @param {function} [ajaxErrorFunction] The function to call on an error AJAX for the retrieved modal's action
 * @returns {Function}
 */
function getModal(modalContainer, removeMceEditors, modalMakerIdPart, ajaxSuccessFunction, ajaxErrorFunction) {
    if (!modalMakerIdPart)
        modalMakerIdPart = 'ModalMaker';
    if (!ajaxSuccessFunction) {
        ajaxSuccessFunction = function () {
            location.reload()
        }
    }
    if (!ajaxErrorFunction) {
        ajaxErrorFunction = function(jqXHR) {
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
    }
    return function () {
        var modalType = $(this).attr('data-modal-operation');
        var target = $(this).attr('data-target');
        var targetId = $(this).attr('data-id');
        var formId = '#' + modalType + modalMakerIdPart;
        var modalMaker = $(formId);
        modalMaker.find('input[name=id]').val(targetId);
        modalMaker.find('input[name=target]').val(target);
        $.ajax({
            type: modalMaker.attr('method'),
            url: modalMaker.attr('action'),
            data: modalMaker.serialize(),
            success: function (resp) {
                if (removeMceEditors) {
                    tinymce.remove();
                }
                // de-register click events and remove previous modals
                modalContainer.find(resp.modal_id).each(function () {
                    $(this).find(resp.form_button).each(function () {
                        $(this).off('click')
                    });
                    $(this).remove();
                });
                modalContainer.append(resp.modal);
                var modal = $(resp.modal_id);

                $(resp.form_button).on('click', getModalSubmitAjax(resp.form_id, ajaxSuccessFunction, ajaxErrorFunction));
                // show tooltips
                modal.find('[data-toggle="tooltip"]').tooltip({
                    trigger: 'hover'
                });
                // Enable the mce editor if we need to
                var mceTexts = [];
                $(resp.form_id).find('textarea').each(function () {
                    if (!($(this).prop('disabled') || $(this).prop('readonly'))) {
                        mceTexts.push(resp.form_id + ' #' + $(this).attr('id'));
                    }
                });
                if (mceTexts.length) {
                    // We have some non-readonly texts
                    enableMCE(mceTexts.join());
                }
                // register reset button
                $('#reset' + modalType.capitalize() + target.capitalize() + 'FormButton').on('click', resetAndClearCreateForm);
                // register add buttons
                enableMultiSelectAdd(modal);
                // find and activate button to enable adding to multi-select
                modal.modal('toggle');
            },
            error: function () {
                alert('Something went wrong!')
            }
        });
    }
}

/**
 * Get the Ajax function to submit a form contained a modal. If there are validation errors, they will be displayed on
 * the form.
 *
 * Successful responses will reset the form and call the success function
 *
 * Unknown errors will create an alert box
 *
 * @param formId The id of the form we are containing
 * @param {callback} ajaxSuccessFunction Function describing action to take on success
 * @param {callback} ajaxErrorFunction Function describing action to take on error
 * @return function a function to submit the modal's form
 */
function getModalSubmitAjax(formId, ajaxSuccessFunction, ajaxErrorFunction) {
    var frm = $(document).find(formId);
    return function () {
        frm.find('textarea').each(function () {
            var c = tinyMCE.get($(this).attr('id'));
            if (c !== null) {
                $(this).html(c.getContent());
            }
        });
        clearFormErrors(frm);
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function (resp) {
                resetForm(frm);
                $('#' + frm.attr('data-containing-modal')).modal('hide');
                ajaxSuccessFunction(resp)
            },
            error: function (jqXHR) {
                ajaxErrorFunction(jqXHR);
            }
        });
    }
}

/**
 * Enable entries to be added to multi-select form fields. This function activates the action on the plus button click
 * and makes sure that a successful entry is inserted into the select input.
 *
 * @param modal The modal to search for multiple select add instances
 */
function enableMultiSelectAdd(modal) {
    var modalAdd = $('#modalAddContainer');
    modal.find('[data-select-related-target]').each(function () {
        var relatedContainer = '#' + $(this).attr('data-select-related-target');
        var ajaxSuccessFunction = function (resp) {
            $(relatedContainer).find('select').first().append($('<option>', {
                value: resp.pk,
                text: resp.string
            }));
        };
        var ajaxErrorFunction = function(jqXHR) {
            if (jqXHR.status === 400) {
                var resp = JSON.parse(jqXHR.responseJSON);
                $.each(resp, function (k, v) {
                    modalAdd.find('#error_' + k).html(v[0].message);
                });
            }
            else {
                alert('Something went wrong!')
            }
        };
        $(this).on('click', getModal(modalAdd, false, 'ModalMakerMulti', ajaxSuccessFunction, ajaxErrorFunction));
    })
}

/**
 * Fix for displaying multiple modal overlays
 * src: https://stackoverflow.com/questions/19305821/multiple-modals-overlay
 */
$(document).ready(function () {
    $(document).on('show.bs.modal', '.modal', function () {
        var zIndex = 1040 + (10 * $('.modal:visible').length);
        $(this).css('z-index', zIndex);
        setTimeout(function () {
            $('.modal-backdrop').not('.modal-stack').css('z-index', zIndex - 1).addClass('modal-stack');
        }, 0);
    });
    $(document).on('hidden.bs.modal', '.modal', function () {
        $('.modal:visible').length && $(document.body).addClass('modal-open');
    });
});