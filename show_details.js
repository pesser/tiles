$(document).ready(
  function() {
  $(document).on(
    "click", ".modal #close, .fadeout",
    function() {
      $(".modal, .fadeout").toggle();
    }
  );

  $(".tilingcontainer .tile").on(
    "click",
    function(e) {
      console.log(
        get_data_for_title($(e.currentTarget).find("h1").text()));
      $(".modal, .fadeout").toggle();
    }
  );
});
