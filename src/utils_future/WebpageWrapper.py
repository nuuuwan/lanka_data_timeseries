from utils_future.Webpage import Webpage


class WebpageWrapper(Webpage):
    def __init__(self, webpage):
        self.url = webpage.url
        self.driver = webpage.driver
        self.width = webpage.width
        self.height = webpage.height
