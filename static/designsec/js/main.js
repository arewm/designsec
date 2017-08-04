modalError = "<p>Uh Oh, something went wrong! Please try refreshing the page. If the problem persists, contact <a href=\"mailto:knox_security@samsung.com\">Knox Security.</a></p>";

var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};
$(document).ready(function () {
    var listLoader = $('#list-maker');
    var category = getUrlParameter('category');
    var categorySorters = $('#category-sorters');
    var categorySelection = categorySorters.children().first();
    if (category) {
        categorySelection = categorySorters.find('#category-'+category);
    }
    $.ajax({
        type: listLoader.attr('method'),
        url: listLoader.attr('action'),
        data: listLoader.serialize(),
        success: function (data) {
            $('#recommendations').html(data);
            categorySelection.addClass('active');
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
                categorySorters.find('li.active').removeClass('active');
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