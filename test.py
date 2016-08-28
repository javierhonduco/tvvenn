from tvvenn import Tvvenn
from json import dumps
from random import choice

if __name__ == '__main__':
    tokens = [
        ('my_token', 'token', \
            'secret'),
    ]
    query = '@unluxo.friends'
    tvvenn = Tvvenn(tokens)
    result = tvvenn.run(query)
    
    ops = tvvenn.test('unluxo') & result 
    screen_names = [user['screen_name'] for user in tvvenn.hydrate(ops)[0]]
    print
    print screen_names
