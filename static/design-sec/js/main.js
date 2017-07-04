$(document).ready(function () {
  $(document).on('click', '.category-sort', function() {
    var cat = $(this).attr('name');
    var frm = $(document).find('#category-selector')
    frm.children("input[name='category']").each(function() {$(this).attr("value")=cat;});

    $.ajax({
      type: frm.attr('method'),
      url: frm.attr('action'),
      data: frm.serialize(),
      success: function (data) {
          $('#list').text()=data;
      },
      error: function (data) {
          alert("Something went wrong!" + data);
      }
    });
  });
});
