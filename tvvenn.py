from parser import Parser
from twitter import TwitterAuth, Fetch, \
        calculate, data_from_id
from utils import divide


class Tvvenn:
    tokens = None
    DEBUG = None

    def __init__(self, tokens, debug=False):
        self.tokens = tokens
        self.DEBUG = debug
        self.tw = TwitterAuth(self.tokens)

    def run(self, unparsed_input):
        fetcher = Fetch(self.tw)
        parser = Parser(fetcher.fetch, calculate)
        return parser.execute(unparsed_input)

    def test(self, screen_name):
        from twitter import get_favorites
        favs = get_favorites(self.tw, screen_name)
        sorted_favs = sorted(favs.items(), key=lambda x: x[1], reverse=True)
        return set([fav[0] for fav in sorted_favs])

    def test2(self, screen_name):
        pass

    def hydrate(self, ids):
        ids = divide(list(ids), 100)
        results = []
        for id in ids:
            result = data_from_id(self.tw, map(str, id))
            results.append(result)
        return results
