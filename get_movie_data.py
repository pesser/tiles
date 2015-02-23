import json
from movie_api import OMDBClient
from trailer_api import YouTubeClient

def get_movies_data(movie_names, cache_filename = "movie_cache.json"):
    try:
        with open(cache_filename, "r") as cache:
            cached_movie_list = json.load(cache)
    except (ValueError, FileNotFoundError):
        print("Movie cache is either corrupted or nonexistent. " +
                "Creating {}".format(cache_filename))
        open(cache_filename, "w").close()
        cached_movie_list = []

    # normalize to lowercase for comparison
    normalized_movie_names = set(movie_name.lower()
            for movie_name in movie_names)
    cached_movie_names = set(movie["Title"].lower()
            for movie in cached_movie_list)

    # remove movies no longer wanted
    unwanted = cached_movie_names - normalized_movie_names
    cached_movie_list = [movie for movie in cached_movie_list
            if movie["Title"].lower() not in unwanted]

    # remove any duplicates that slipped in
    known = set()
    unique_movies = 0
    for movie in cached_movie_list:
        if movie["Title"].lower() not in known:
            known.add(movie["Title"].lower())
            cached_movie_list[unique_movies] = movie
            unique_movies += 1
    print("Removing {} duplicates.".format(
        len(cached_movie_list) - unique_movies))
    del cached_movie_list[unique_movies:]
        
    # movies not yet cached
    movies_to_get = normalized_movie_names - cached_movie_names
    client = OMDBClient()
    youtube_client = YouTubeClient()
    print("Obtaining informations...")
    for movie in movies_to_get:
        title = [movie_name for movie_name in movie_names if
                movie_name.lower() == movie][0]
        print(title)
        info = client.query(title, False)
        if "Error" in info:
            print("Could not retrieve information for '{}'.".format(title) +
                    " Skipping.")
        else:
            youtube_link = ("www.youtube.com" +
                    youtube_client.query(info["Title"])[0])
            info["YoutubeTrailer"] = youtube_link
            cached_movie_list.append(info)

    with open(cache_filename, "w") as cache:
        json.dump(cached_movie_list, cache)

    return cached_movie_list
