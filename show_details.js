$(document).ready(
  function() {
  $(".modal, .fadeout").hide();

  $(document).on(
    "click", ".modal #close, .fadeout",
    function() {
      $(".modal #trailer").empty();
      $(".modal, .fadeout").toggle();
    }
  );

  $(".tilingcontainer .tile").on(
    "click",
    function(e) {
      $(".modal, .fadeout").toggle();
      movie_data = get_data_for_title($(e.currentTarget).find("#title").text());
      var content = $(".modal .content");
      content.find("#title").text(movie_data["Title"]);
      var info = content.find("#info");
      info.empty();
      info.append($("<dl>"));

      keys = ["Genre", "Year", "Nokey", "Country", "Director", "Writer",
        "Plot", "Actors", "Metascore", "imdbRating"];
      for(var i in keys) {
        var k = keys[i];
        var val = movie_data[k];

        // skip if requested data is not available
        if(!val) continue;

        if(movie_data[k] instanceof Array) {
          val = movie_data[k].join(", ");
        }
        info.append($("<dt>", {"text": k}));
        info.append($("<dd>", {"text": val}));
      }

      var youtube = movie_data["YoutubeTrailer"];
      console.log(youtube);
      var id_matcher = /watch\?v=(.+)/;
      var youtubeId = youtube.match(id_matcher)[1];
      console.log(youtubeId);
      var youtubeUrl = ("http://www.youtube.com/embed/" + youtubeId +
                        "?autoplay=1&html5=1");
      content.find("#trailer").empty().append(
        $("<iframe>",
          {"id": "youtubeframe", "type": "text-html",
            "src": youtubeUrl}));
    }
  );
});
