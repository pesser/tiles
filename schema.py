class Movie(object):
    def __init__(
            self,
            title = "",
            poster_image_url = "",
            trailer_youtube_url = "",
            optional_data = None):
        self.title = title
        self.poster_image_url = poster_image_url
        self.trailer_youtube_url = trailer_youtube_url
        self.optional_data = optional_data or {}
