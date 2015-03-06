import json
from html.parser import HTMLParser
try:
    import httplib
except ImportError:
    import http.client as httplib

class OMDBClient(object):
    def __init__(self):
        self.api_entry = "www.omdbapi.com"
        self.headers = {"Accept":"application/json",
                        "Accept-Charset":"utf-8"}

    def query(self, title, rt = True):
        body = {"t": title, "tomatoes": rt}
        json_body = json.dumps(body)
        params = []
        for k, v in body.items():
            if isinstance(v, str):
                v = v.replace(" ", "%20")
            params.append("{}={}".format(k, v))
        url = "/?" + "&".join(params)
        connection = httplib.HTTPConnection(self.api_entry)
        connection.set_debuglevel(0)
        print(self.api_entry + url)
        connection.request(
                method = "GET",
                url = url,
                headers = self.headers)
        str_response = connection.getresponse().read().decode("utf-8")
        try:
            return json.loads(str_response)
        except:
            print("Could not decode response.")
            print(str_response)
            return str_response

class VideoFinder(HTMLParser):
    def __init__(self):
        self.results = []
        super(VideoFinder, self).__init__()

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            dict_attrs = dict(attrs)
            if "href" in dict_attrs:
                if "/watch?v=" in dict_attrs["href"]:
                    self.results.append(dict_attrs["href"])

    def clear(self):
        self.results = []


class YouTubeClient(object):
    def __init__(self):
        self.api_entry = "www.youtube.com"
        self.headers = {"Accept": "text/html", "Accept-Charset":"utf-8"}
        self.parser = VideoFinder()

    def query(self, title):
        body = {"search_query": title + " trailer"}
        
        params = []
        for k, v in body.items():
            v = v.replace(" ", "%20")
            params.append("{}={}".format(k, v))

        url = "/results?" + "&".join(params)
        # must use https as youtube redirects everything to 443
        connection = httplib.HTTPSConnection(self.api_entry)
        connection.set_debuglevel(0)
        print(self.api_entry + url)
        connection.request(
                method = "GET",
                url = url,
                headers = self.headers)
        str_response = connection.getresponse().read().decode("utf-8")

        self.parser.clear()
        self.parser.feed(str_response)

        return list(self.parser.results)

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
    normalized_movie_names = list(movie_name.lower()
            for movie_name in movie_names)
    cached_movie_names = list(movie["Title"].lower()
            for movie in cached_movie_list)

    # remove movies no longer wanted
    cached_movie_list = [movie for movie in cached_movie_list
            if movie["Title"].lower() in normalized_movie_names]

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
    movies_to_get = list(movie_name for movie_name in movie_names if
            movie_name.lower() not in cached_movie_names)
    client = OMDBClient()
    youtube_client = YouTubeClient()
    print("Obtaining data...")
    for title in movies_to_get:
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
