from schema import Movie
from fresh_tomatoes import open_movies_page
from template import (DocumentTemplate, TilingTemplate, make_description,
        link)
from movie_api import OMDBClient

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

#open_movies_page(movie_list)
movie_list = 5 * movie_list

movie_list = []
client = OMDBClient()
movie_names = ["True Romance", "The Matrix"]
for name in movie_names:
    info = client.query(name, False)
    if "Error" in info:
        print("Could not retrieve information for '{}'.".format(name) +
                " Skipping.")
    else:
        movie = Movie(
                title = info.pop("Title"),
                poster_image_url = info.pop("Poster"),
                trailer_youtube_url = "unknown",
                optional_data = info)
        movie_list.append(movie)



base = DocumentTemplate("base.template.html")
base.add_stylefile("description.css")
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
