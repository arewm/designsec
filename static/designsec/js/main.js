function toggleIcon(e) {
    $(e.target)
        .prev('.panel-heading')
        .find('.more-less')
        .toggleClass('glyphicon-plus glyphicon-minus');
}

$(document).ready(function () {
    var listLoader = $('#list-maker');
    $.ajax({
        type: listLoader.attr('method'),
        url: listLoader.attr('action'),
        data: listLoader.serialize(),
        success: function (data) {
                $('#recommendations').html(data);
                $('#category-sorters').children().first().addClass('active')
        },
        error: function (data) {
                alert("Something went wrong!" + data);
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

                // register the new show/hide clicks
                $('.panel-group').on('hide.bs.collapse', toggleIcon);
                $('.panel-group').on('show.bs.collapse', toggleIcon);
            },
            error: function (data) {
                alert("Something went wrong!" + data);
            }
        });
    });

    // todo make a function to roll up/down each field
});