$(document).ready(function () {
    // enable modals
    var modalContainer = $('#modalContainer');
    $('.modal-operation').on('click', getModal(modalContainer));
    $(document).on('click', '.category-sort', registerSortOnCategory(function (recommendation) {
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
    }));
})