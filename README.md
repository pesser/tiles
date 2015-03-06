# Movie Trailer Website

## About
This is an implementation of the first project within
[Udacity](https://www.udacity.com/)'s [Full Stack Web
Devloper Nanodegree](https://www.udacity.com/course/nd004). It represents
server-side code to store movies and generate a web page representation of
these. The latest version is available on
[GitHub](https://github.com/pesser/tiles).


## Useage
Running `generate.py` with your favourite __Python 3.0__ implementation
generates `index.html`. Open this file with a browser to see different film
posters. Hover over a poster to see the film's title and some basic
information.  Upon clicking, a modal containing an embedded video
of the film's trailer as well as detailed data is opened.

Tested with [CPython
3.4.2](https://www.python.org/download/releases/3.4.2/),
[Chromium 40](http://www.chromium.org/Home) and [Firefox
35](https://www.firefox.com/).


## Showcase
![Screenshot](screenshot.png)
[Demo](http://pesser.github.io/tiles/)


## Customization
`generate.py` contains a list of movie names. For each of the movies it will
try to obtain information from the [OMDb API](http://omdbapi.com/) as well
as from [YouTube](https://www.youtube.com/). If data can not be
retrieved, the movie will be ignored. However, to avoid excessive data
requests, the movies' data is stored on disc in
[JSON](http://tools.ietf.org/html/rfc7159) format, which allows
you to manually insert data. Similiarly, the movies' posters are retrieved
and stored in the folder `posters`, since [IMDb](http://www.imdb.com/) does
not allow hotlinking.

The repository contains the cached data for an example list of movies, as
well as the corresponding posters. To generate a web page for other movies,
just change the list of movie names in `generate.py` and run it again.

Some design aspects of the generated web page can be adjusted through the
methods of the `TilingTemplate` instance. In particular, the width of the
container holding the posters and the number of posters per row can be
adjusted to generate versions for different resolutions.
