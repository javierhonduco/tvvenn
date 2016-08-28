from twython import Twython
from random import choice
from utils import timer


class Logger:
    def info(string):
        pass

logger = Logger()

COUNT = 2000


def get_friends(tw, name):
    # logger.info('get_friends called')
    tw = tw.authorize()
    with timer(logger.info):
        ids = [user for user in tw.cursor(tw.get_friends_ids,
            screen_name=name, count=COUNT)]
    return set(ids)


def get_favorites(tw, name):
    tw = tw.authorize()
    ids = [user['user']['id'] for user in tw.get_favorites(screen_name=name, count=200)]
    favs = {}
    for id in ids:
        if id not in favs:
            favs[id] = 1
        else:
            favs[id] += 1

    return favs


def get_followers(tw, name):
    # logger.info('get_followers called')
    tw = tw.authorize()
    with timer(logger.info):
        ids = [user for user in tw.cursor(tw.get_followers_ids,
            screen_name=name, count=COUNT)]
    return set(ids)


def data_from_id(tw, ids):
    # logger.info('data_from_id called')
    tw = tw.authorize()
    result = None
    with timer(logger.info):
        result = tw.lookup_user(user_id=ids)
    return result


class TwitterAuth:
    tokens = None

    def __init__(self, tokens):
        self.tokens = tokens

    def authorize(self):
        name, app_key, app_secret = choice(self.tokens)
        # logger.info('token with name {name} chosen'.format(name=name))
        twitter = Twython(app_key, app_secret, oauth_version=2)
        access_token = twitter.obtain_access_token()
        return Twython(app_key, access_token=access_token)


class Fetch:
    tw = None

    def __init__(self, tw):
        self.tw = tw

    def fetch(self, name, op):
        tw = self.tw

        if op == 'friends':
            return get_friends(tw, name)
        elif op == 'followers':
            return get_followers(tw, name)
        elif op == 'all':
            return get_followers(tw, name) | get_friends(tw, name)
        elif op == 'mutual':
            return get_followers(tw, name) & get_friends(tw, name)
        elif op == 'ego':
            return get_followers(tw, name) - get_friends(tw, name)
        return set([])


def calculate(start, pairs):
    result = start
    for op, value in pairs: 
        if op == '&':   
            result &= value
        elif op == '|':
            result |= value
        elif op == '-':
            result -= value
        elif op == '^':
            result ^= value
    return result
