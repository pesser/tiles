from schema import Movie
from fresh_tomatoes import open_movies_page
from template import (DocumentTemplate, TilingTemplate, make_description,
        link)
from get_movie_data import get_movies_data

movie_list = [
        Movie(
            title = "The Matrix",
            poster_image_url =
            "http://ia.media-imdb.com/images/M/MV5BMTkxNDYxOTA4M15BMl5BanBnXkFtZTgwNTk0NzQxMTE@._V1_SX214_AL_.jpg",
            trailer_youtube_url =
            "https://www.youtube.com/watch?v=m8e-FF8MsqU"),
        Movie(
            title = "True Romance",
            poster_image_url =
            "http://ia.media-imdb.com/images/M/MV5BMTMxMTM3MDIwM15BMl5BanBnXkFtZTcwMDYyOTUyMg@@._V1_SX214_AL_.jpg",
            trailer_youtube_url =
            "https://www.youtube.com/watch?v=_wNYNDzKpuQ"),
        Movie(
            title = "Ghost in the Shell",
            poster_image_url =
            "http://ia.media-imdb.com/images/M/MV5BMTk2ODE4MDUzNF5BMl5BanBnXkFtZTYwNTI2OTA5._V1_SY317_CR5,0,214,317_AL_.jpg",
            trailer_youtube_url =
            "https://www.youtube.com/watch?v=SvBVDibOrgs"),
        Movie(
            title = "Spirited Away",
            poster_image_url =
            "http://ia.media-imdb.com/images/M/MV5BMjYxMDcyMzIzNl5BMl5BanBnXkFtZTYwNDg2MDU3._V1_SY317_CR5,0,214,317_AL_.jpg",
            trailer_youtube_url =
            "https://www.youtube.com/watch?v=ByXuk9QqQkk")
        ]

cache_filename = "movie_cache.json"

movie_names = {"True Romance", "The Matrix", "Spirited Away",
"The Grand Budapest Hotel", "Fantastic Mr. Fox",
"Charlie and the Chocolate Factory", "My Neighbor Totoro",
"Little Miss Sunshine", "Her", "Brazil", "Synecdoche, New York",
"Ghost in the Shell", "Moon", "American Beauty", "Network",
"King of California", "One Flew over the Cuckoo's Nest", "Blade Runner",
"2001: A Space Odyssey", "Tron: Legacy", "A Serious Man", "Existenz",
"Fight Club", "Eraserhead", "Naked Lunch", "My Life as a Dog",
"Soul Kitchen", "The Big Lebowski", "Being John Malkovich",
"Pulp Fiction"}

movie_list = []
movie_data_list = get_movies_data(movie_names, cache_filename)
for movie_data in movie_data_list:
    movie = Movie(
            title = movie_data.pop("Title"),
            poster_image_url = movie_data.pop("Poster"),
            trailer_youtube_url = "unknown",
            optional_data = movie_data)
    movie_list.append(movie)

base = DocumentTemplate("base.template.html")
base.add_stylefile("description.css")
base.add_stylefile("modal.css")
tiling = TilingTemplate(base, "tiling.template.css", "tile.template.html")
for movie in movie_list:
    tiling.add_tile(
            movie.poster_image_url,
            make_description(
                movie.title,
                **movie.optional_data
                )
            )
tiling.write()
