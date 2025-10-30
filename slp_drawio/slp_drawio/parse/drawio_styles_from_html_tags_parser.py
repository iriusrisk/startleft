from html.parser import HTMLParser

DRAWIO_FONT_STYLE_KEY = 'fontStyle'
DRAWIO_FONT_COLOR_KEY = 'fontColor'
DRAWIO_FONT_FAMILY_KEY = 'fontFamily'
DRAWIO_FONT_SIZE_KEY = 'fontSize'



def _sum_drawio_font_styles(styles):
    font_style_sum = 0
    result = []

    for item in styles:
        key, value = item.split('=', 1)
        key = key.strip()
        value = value.strip()

        if key == DRAWIO_FONT_STYLE_KEY:
            font_style_sum += int(value)
        else:
            result.append(f'{key}={value}')

    if font_style_sum:
        result.insert(0, f'{DRAWIO_FONT_STYLE_KEY}={font_style_sum}')

    return result



class DrawioStylesFromHtmlTagsParser(HTMLParser):


    def __init__(self):
        super().__init__()
        self.styles = []

    def parse(self, html: str) -> list[str]:
        """
        Parses the given HTML string and extracts Drawio-compatible styles.
        :param html: The HTML string to parse.
        :return: A list of Drawio-compatible style strings.
        """
        self.styles = []
        self.feed(html)
        return _sum_drawio_font_styles(self.styles)

    def handle_starttag(self, tag, attrs):
        """
            Handles an HTML tag and extracts styles.

            Drawio uses specific CSS styles for formatting:
            Style	        fontStyle
            Bold	        1
            Italic	        2
            Underline	    4
            Strikethrough	8
            All of them combined: sum of values (e.g., Bold + Italic + Underline + Strikethrough = 15)
        """
        if tag == "b":
            self.styles.append(f"{DRAWIO_FONT_STYLE_KEY}= 1")
        elif tag == "i":
            self.styles.append(f"{DRAWIO_FONT_STYLE_KEY}= 2")
        elif tag == "u":
            self.styles.append(f"{DRAWIO_FONT_STYLE_KEY}= 4")
        elif tag == "strike" or tag == "s":
            self.styles.append(f"{DRAWIO_FONT_STYLE_KEY}= 8")
        elif tag == "font":
            attr_dict = dict(attrs)
            if "color" in attr_dict:
                self.styles.append(f"{DRAWIO_FONT_COLOR_KEY}= {attr_dict['color']}")
            if "face" in attr_dict:
                self.styles.append(f"{DRAWIO_FONT_FAMILY_KEY}= {attr_dict['face']}")
