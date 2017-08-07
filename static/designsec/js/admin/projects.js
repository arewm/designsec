$(document).ready(function () {
    // enable modals
    var modalContainer = $('#modalContainer');
    $('.modal-operation').on('click', getModal(modalContainer));

    var onLoadAction = function(recommendation) {
        // enable modals to be loaded for the new content
        recommendation.find('.modal-operation').each(function () {
            $(this).on('click', getModal(modalContainer));
        });
        // allow recommendation edits to be saved for new content
        recommendation.find('.save-recommendations').each(function () {
            $(this).on('click', function () {
                var frm = $('#saveProjectRecommendations');
                $.ajax({
                    type: frm.attr('method'),
                    url: frm.attr('action'),
                    data: frm.serialize(),
                    success: function (data) {
                        recommendation.html(data);
                        recommendation.find('[data-toggle="tooltip"]').tooltip({
                            trigger: 'hover'
                        });
                        recommendation.find('.modal-operation').each(function () {
                            $(this).on('click', getModal(modalContainer));
                        });
                    },
                    error: function () {
                        alert('Something went wrong!')
                    }
                });
            })
        })
    };
    var beforeSubmitAction = function(selection, categorySorters, recommendations) {
        var cat = selection.attr('data-pk');
        var frm = $(document).find('#saveProjectRecommendations');
        frm.find('[name=category]').attr('value', cat);
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function (data) {
                recommendations.html(data);
                recommendations.find('[data-toggle="tooltip"]').tooltip({
                    trigger: 'hover'
                });
                onLoadAction(recommendations);
                categorySorters.find('li.active').removeClass('active');
                selection.addClass('active');
            },
            error: function (data) {
                $('#errorModalText').html(modalError);
                $('#errorModal').modal('show');
            }
        });
        return false
    };
    $(document).on('click', '.category-sorters', registerSortOnCategory(onLoadAction, beforeSubmitAction));
});