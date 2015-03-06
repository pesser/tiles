$(document).ready(
  function() {
  $(".modal, .fadeout").hide();

  // only show a subset of the data
  var keysToShow = ["Year", "Director", "Genre"];
  $(".description dt").filter(function(index) {
    return keysToShow.indexOf(this.textContent) == -1;
  }).hide().next("dd").hide();

  // modal closing
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
      var movie_repr = $(e.currentTarget);
      var content = $(".modal .content");
      content.find(".title").text(movie_repr.find(".title").text());
      var info = content.find("#info");
      info.empty();
      var info_list = $("<dl>");
      info.append(info_list);

      keys = ["Genre", "Year", "Nokey", "Country", "Director", "Writer",
        "Plot", "Actors", "Metascore", "imdbRating"];
      for(var i in keys) {
        var k = keys[i];
        var val = movie_repr.find("dt:contains('" + k + "')").next("dd").text();

        // skip if requested data is not available
        if(!val) continue;

        info_list.append($("<dt>", {"text": k}));
        info_list.append($("<dd>", {"text": val}));
      }

      // show trailer if available
      var trailer_container = content.find("#trailer");
      trailer_container.empty().parent().hide();

      var youtube_key = movie_repr.find("dt:contains('youtube_trailer')");
      if(youtube_key.length == 1) {
        var youtube = youtube_key.next("dd").text();
        var id_matcher = /watch\?v=(.+)/;
        var youtubeIdMatch = youtube.match(id_matcher);
        if(youtubeIdMatch && youtubeIdMatch.length == 2) {
          var youtubeId = youtubeIdMatch[1];
          var youtubeUrl = ("http://www.youtube.com/embed/" + youtubeId +
                            "?autoplay=1&html5=1");
          trailer_container.append(
            $("<iframe>",
              {"id": "youtubeframe", "type": "text-html",
                "src": youtubeUrl}));
          trailer_container.parent().show();
        }
      }
    }
  );
});
