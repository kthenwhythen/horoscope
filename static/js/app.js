// Ajax with animation for card-today
$(document).ready(
  $("#card-hide-today").on( "click",
    function () {
      $(this).css('opacity', '0');
      $("#card-body").css('max-height', '1000px');
      $.get("/prediction/today", function(data, status){
        $("#card-text-today").text(data);
      });
    }
  )
);
