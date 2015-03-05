class Movie(object):
    def __init__(
            self,
            title,
            poster_image_url,
            youtube_trailer,
            optional_data = None):
        self.title = title
        self.poster_image_url = poster_image_url
        self.youtube_trailer = youtube_trailer
        self.optional_data = optional_data or {}
