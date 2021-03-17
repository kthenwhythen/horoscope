//////// Cards ajax

// Ajax with animation for card-yesterday
$(document).ready(
  $("#card-hide-yesterday").on("click",
    function () {
      $("#card-hide-wrap-yesterday").hide();
      $.ajax({
        url: "/prediction/yesterday",
        beforeSend: function () {
          $('#loader-yesterday').show();
        },
        complete: function () {
          $("#card-hide-yesterday").css('opacity', '0');
        },
        success: function (data, date) {
          $("#card-body-yesterday").css('max-height', '600px');
          $("#card-text-yesterday").text(data);
          $("#date-yesterday").text(date);
        }
      });
    }
  )
);

// Ajax with animation for card-today
$(document).ready(
  $("#card-hide-today").on("click",
    function () {
      $("#card-hide-wrap-today").hide();
      $.ajax({
        url: "/prediction/today",
        beforeSend: function () {
          $('#loader-today').show();
        },
        complete: function () {
          $("#card-hide-today").css('opacity', '0');
        },
        success: function (data) {
          $("#card-body-today").css('max-height', '600px');
          $("#card-text-today").text(data);
        }
      });
    }
  )
);

// Ajax with animation for card-tomorrow
$(document).ready(
  $("#card-hide-tomorrow").on("click",
    function () {
      $("#card-hide-wrap-tomorrow").hide();
      $.ajax({
        url: "/prediction/tomorrow",
        beforeSend: function () {
          $('#loader-tomorrow').show();
        },
        complete: function () {
          $("#card-hide-tomorrow").css('opacity', '0');
        },
        success: function (data) {
          $("#card-body-tomorrow").css('max-height', '600px');
          $("#card-text-tomorrow").text(data);
        }
      });
    }
  )
);

//////// Menu btns

// Yesterday btn
$(document).ready(
  $("#yesterday-btn").on("click",
    function () {
      $("#yesterday-btn").addClass("active")
      $("#today-btn").removeClass("active")
      $("#tomorrow-btn").removeClass("active")

      $("#card-yesterday").show()
      $("#card-today").hide()
      $("#card-tomorrow").hide()
    }
  )
);

// Today btn
$(document).ready(
  $("#today-btn").on("click",
    function () {
      $("#yesterday-btn").removeClass("active")
      $("#today-btn").addClass("active")
      $("#tomorrow-btn").removeClass("active")

      $("#card-yesterday").hide()
      $("#card-today").show()
      $("#card-tomorrow").hide()
    }
  )
);

// Tomorrow btn
$(document).ready(
  $("#tomorrow-btn").on("click",
    function () {
      $("#yesterday-btn").removeClass("active")
      $("#today-btn").removeClass("active")
      $("#tomorrow-btn").addClass("active")

      $("#card-yesterday").hide()
      $("#card-today").hide()
      $("#card-tomorrow").show()
    }
  )
);
