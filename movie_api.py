import json
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

