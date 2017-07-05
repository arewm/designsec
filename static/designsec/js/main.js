$(document).ready(function () {
    var listLoader = $('#list-maker');
    $.ajax({
        type: listLoader.attr('method'),
        url: listLoader.attr('action'),
        data: listLoader.serialize(),
        success: function (data) {
                $('#recommendations').text = data;
        },
        error: function (data) {
                alert("Something went wrong!" + data);
        }
    });

    $(document).on('click', '.category-sort', function () {
        var cat = $(this).text();
        var frm = $(document).find('#category-selector');
        $("#category-sort").attr("value", cat);
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function (data) {
                $('#recommendations').text = data;
            },
            error: function (data) {
                alert("Something went wrong!" + data);
            }
        });
    });

    // todo make a function to roll up/down each field
});
