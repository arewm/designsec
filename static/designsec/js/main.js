modalError = "<p>Uh Oh, something went wrong! Please try refreshing the page. If the problem persists, contact <a href=\"mailto:knox_security@samsung.com\">Knox Security.</a></p>";
$(document).ready(function () {
    var listLoader = $('#list-maker');
    $.ajax({
        type: listLoader.attr('method'),
        url: listLoader.attr('action'),
        data: listLoader.serialize(),
        success: function (data) {
            $('#recommendations').html(data);
            $('#category-sorters').children().first().addClass('active');
        },
        error: function (data) {
            $('#errorModalText').html(modalError);
            $('#errorModal').modal('show');
        }
    });

    $(document).on('click', '.category-sort', function () {
        var selection = $(this);
        //var cat = selection.text();
        var cat = selection.attr('id').split('-')[1];
        var frm = $(document).find('#category-selector');
        $("#category-sort").attr("value", cat);
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function (data) {
                $('#recommendations').html(data);
                $('#category-sorters').find('li.active').removeClass('active');
                selection.addClass('active');
            },
            error: function (data) {
                $('#errorModalText').html(modalError);
                $('#errorModal').modal('show');
            }
        });
    });
    $('#reloadButton').on('click', function(e) {
        window.location.reload();
    });
});