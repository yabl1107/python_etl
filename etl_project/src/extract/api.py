from .base import BaseExtractor


class APIExtractor(BaseExtractor):
    def __init__(self, fetcher=None):
        self.fetcher = fetcher

    def extract(self):
        if callable(self.fetcher):
            return self.fetcher()
        return []


def extract_from_api(fetcher=None):
    extractor = APIExtractor(fetcher=fetcher)
    return extractor.extract()
