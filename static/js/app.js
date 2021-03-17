// Ajax with animation for card-today
$(document).ready(
  $("#card-hide-today").on("click",
    function () {
      $(".card-hide-wrap").hide();
      $.ajax({
        url: "/prediction/today",
        beforeSend: function () {
          $('#loader').show();
        },
        complete: function () {
          $("#card-hide-today").css('opacity', '0');
        },
        success: function (data) {
          $("#card-body").css('max-height', '600px');
          $("#card-text-today").text(data);
        }
      });
    }
  )
);
