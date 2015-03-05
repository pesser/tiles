$(document).ready(
  function() {
  $(".modal, .fadeout").hide();

  // only show a subset of the data
  var keysToShow = ["Year", "Director", "Genre"];
  $(".description dt").filter(function(index) {
    return keysToShow.indexOf(this.innerText) == -1;
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
      content.find("#title").text(movie_repr.find("#title").text());
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

      var youtube = (movie_repr.find("dt:contains('youtube_trailer')").
        next("dd").text());
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
