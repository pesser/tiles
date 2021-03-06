import math
import re

# formatter to be able to use ${} replacement in order to avoid
# conflict between javascript templates and pythons {} replacement
class Formatter(object):
    delimiter = re.compile(r"""\$\{(\w+)\}""")
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def replace(self, match):
        key = match.group(1)
        return str(self.kwargs[key])

    def format(self, toformat):
        return self.delimiter.sub(self.replace, toformat)

def read_template(filename):
    template = ""
    with open(filename, "r") as infile:
        template = infile.read()
    return template

def format_template(template, **kwargs):
    formatter = Formatter(**kwargs)
    return formatter.format(template)

# read a template, substitute all ${} placeholders with the corresponding
# value of the kwarg provided, write the result to a file where ".template"
# is removed from the original filename
def write_template(filename, **kwargs):
    assert(".template" in filename)
    final_filename = filename.replace(".template", "")
    template = read_template(filename)
    with open(final_filename, "w") as outfile:
        outfile.write(format_template(template, **kwargs))
    return final_filename
    
# base template for html document. The template file must contain the
# ${body} and ${head} indicators.
# Can add css files, javascript and arbitrary body contents.
class DocumentTemplate(object):
    def __init__(self, template_filename):
        self.template_filename = template_filename
        self.stylefiles = []
        self.js_sources = []
        self.body_contents = []
        self.finalized = False

    def add_stylefile(self, stylefile):
        self.stylefiles.append(stylefile)

    def add_js(self, js_source):
        self.js_sources.append(js_source)

    def add_body(self, body):
        self.body_contents.append(body)

    def write(self):
        return write_template(self.template_filename,
                head = self.make_head(),
                body = self.make_body())

    # internal
    def make_head(self):
        header = ""
        for stylefile in self.stylefiles:
            header += (
                    '''<link rel="stylesheet" type="text/css" ''' +
                    '''href="{cssfile}">\n''').format(cssfile = stylefile)
        for source in self.js_sources:
            header += '''<script src="{}"></script>\n'''.format(source)
        return header

    def make_body(self):
        return "\n".join(self.body_contents)

        
# add a tiling design to a given base template.
class TilingTemplate(object):
    def __init__(self,
            document_base,
            style_template_filename,
            tile_template_filename):
        self.document_base = document_base
        self.style_template_filename = style_template_filename
        self.style_template = read_template(style_template_filename)
        self.tile_template = read_template(tile_template_filename)
        self.finalized = False
        self.tile_htmls = []

        # defaults
        self.container_width = 800
        self.nr_tiles = 5
        self.ar = 0.66875
        self.border_width = 2

    def set_container_width(self, width):
        self.container_width = width

    # nr of tiles per row
    def set_nr_tiles(self, nr_tiles):
        self.nr_tiles = nr_tiles

    # aspect ratio of tiles
    def set_ar(self, ar):
        self.ar = ar

    def set_border_width(self, bw):
        self.border_width = 2

    def add_tile(self, img_src, alt_txt, content):
        tile_html = format_template(self.tile_template, 
                tile_img_src = img_src,
                alt_txt = alt_txt,
                tile_hover_content = content)
        self.tile_htmls.append(tile_html)

    def write(self):
        if not self.finalized:
            self.finalize()
        self.document_base.write()

    # internal
    def finalize(self):
        self.finalize_style()
        self.finalize_tiles()
        self.finalized = True

    def finalize_sizes(self):
        self.tile_width = math.floor(self.container_width / self.nr_tiles)
        self.tile_height = round(self.tile_width / self.ar)

    def finalize_style(self):
        self.finalize_sizes()
        style_filename = write_template(
                self.style_template_filename,
                container_width = self.container_width,
                tile_width = self.tile_width,
                tile_height = self.tile_height,
                tile_hover_width = self.tile_width - 2*self.border_width,
                tile_hover_height = self.tile_height - 2*self.border_width,
                tile_hover_border_width = self.border_width)
        self.document_base.add_stylefile(style_filename)

    def finalize_tiles(self):
        container_begin = ["""<div class="tilingcontainer">"""]
        container_end = ["""</div>"""]
        tile_html = "\n".join(
                container_begin + self.tile_htmls + container_end)
        self.document_base.add_body(tile_html)
