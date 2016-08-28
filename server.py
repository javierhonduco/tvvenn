from tvvenn import Tvvenn
from wsgiref.simple_server import make_server
from cgi import parse_qs, escape

import json

from ometa.runtime import ParseError
from twython.exceptions import TwythonRateLimitError, TwythonError

tokens = [
    ('leaked_android', 'IQKbtAYlXLripLGPWd0HUA',
        'GgDYlkSvaPxGxC4X8liwpUoqKwwr3lCADbz8A7ADU'),
    ('leaked_random', '3nVuSoBZnx6U4vzUxf5w',
        'Bcs59EFbbsdF6Sl9Ng71smgStWEGwXXKSjYvPVt7qys'),
    ('leaked_ios?', 'iAtYJ4HpUVfIUoNnif1DA',
        '172fOpzuZoYzNYaU3mMYvE8m8MEyLbztOdbrUolU')
]


def app(environ, start_response):
    get_data = parse_qs(environ['QUERY_STRING'])

    query = escape(get_data.get('query', [''])[0])
    hydrated = escape(get_data.get('hydrated', [''])[0])

    status = '200 OK'
    response_headers = [('Content-type', 'application/json')]
    response = []
    result = set()

    try:
        tvvenn = Tvvenn(tokens)
        response = list(tvvenn.run(query))

        if hydrated == 'true':
            response = tvvenn.hydrate(response)

        result = {
            'status': 'success',
            'data': response
        }
    except ParseError as e:
        status = '500 ERROR'
        result = {
            'status': 'error',
            'data': 'Parse error. {tb}'.format(tb=e)
        }
    except TwythonRateLimitError as e:
        status = '500 ERROR'
        result = {
            'status': 'error',
            'data': 'Been throttled'
        }
    except TwythonError as e:
        status = '500 ERROR'
        result = {
            'status': 'error',
            'data': 'Tw user does not exists'
        }
    except Exception as e:
        status = '500 ERROR'
        result = {
            'status': 'error',
            'data': 'Unknown error: {e}'.format(e=e)
        }

    start_response(status, response_headers)
    return [json.dumps(result)]

if __name__ == '__main__':
    port = 8000

    print 'Server started @ {port}'.format(port=port)
    server = make_server('', port, app)
    server.serve_forever()
