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
    $('.add-project').on('click', getModal());
    $('.delete-project').on('click', getModal());;
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
    $(document).on('hidden.bs.modal', function () {
        clearFormErrors($(this).find('form'))
    });
});