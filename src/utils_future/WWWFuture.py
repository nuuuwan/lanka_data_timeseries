import requests


class WWWFuture:
    @staticmethod
    def join(*url_list):
        return '/'.join(url_list)

    @staticmethod
    def get_json(url):
        return requests.get(url).json()
