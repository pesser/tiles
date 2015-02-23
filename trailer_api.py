from html.parser import HTMLParser
try:
    import httplib
except ImportError:
    import http.client as httplib

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
