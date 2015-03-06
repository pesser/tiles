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

    def text_html(self):
        html = '''<div class="description">\n'''
        html += '''<h1 class="title">{}</h1>\n'''.format(self.title)
        html += '''<dl>\n'''
        html += '''<dt>{}</dt><dd>{}</dd>\n'''.format(
                "youtube_trailer",
                self.youtube_trailer)
        if len(self.optional_data) > 0:
            for k, v in self.optional_data.items():
                if isinstance(v, list):
                    v = ", ".join(v)
                html += '''<dt>{}</dt><dd>{}</dd>\n'''.format(k, v)
        html += '''</dl>\n'''
        html += "</div>"
        return html
