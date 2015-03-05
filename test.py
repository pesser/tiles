from schema import Movie
from template import (DocumentTemplate, TilingTemplate,
        make_description, write_template)
from get_movie_data import get_movies_data
import json

movie_names = ["True Romance", "The Matrix", "Spirited Away",
"The Grand Budapest Hotel", "Fantastic Mr. Fox",
"Charlie and the Chocolate Factory", "My Neighbor Totoro",
"Little Miss Sunshine", "Her", "Brazil", "Synecdoche, New York",
"Ghost in the Shell", "Moon", "American Beauty", "Network",
"King of California", "One Flew over the Cuckoo's Nest", "Blade Runner",
"2001: A Space Odyssey", "Tron: Legacy", "A Serious Man", "Existenz",
"Fight Club", "Eraserhead", "Naked Lunch", "My Life as a Dog",
"Soul Kitchen", "The Big Lebowski", "Being John Malkovich",
"Pulp Fiction"]

# use this file as a manually managed cache to avoid too much data scraping
cache_filename = "movie_cache.json"

movie_list = []
movie_data_list = get_movies_data(movie_names, cache_filename)
# json dump of the movies' data to pass data to javascript
movie_data_json = json.dumps(movie_data_list)
for movie_data in movie_data_list:
    movie = Movie(
            title = movie_data.pop("Title"),
            poster_image_url = movie_data.pop("Poster"),
            youtube_trailer = movie_data.pop("YoutubeTrailer"),
            optional_data = movie_data)
    movie_list.append(movie)

base = DocumentTemplate("base.template.html")
base.add_stylefile("description.css")
base.add_stylefile("modal.css")
base.add_js("http://code.jquery.com/jquery-1.10.1.min.js")
# inject movie data into script
base.add_js(
        write_template(
            "get_data.template.js",
            json_data = movie_data_json))
base.add_js("show_details.js")

# make tiles of movie posters
tiling = TilingTemplate(base, "tiling.template.css", "tile.template.html")
for movie in movie_list:
    tiling.add_tile(
            movie.poster_image_url,
            make_description(
                movie.title,
                youtube_trailer = movie.youtube_trailer,
                **movie.optional_data
                )
            )
tiling.write()
