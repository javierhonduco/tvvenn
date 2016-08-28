
![Alt](https://raw.githubusercontent.com/javierhonduco/tvvenn/master/art/logo.png)
==================================================================================

Set operations – on twitter.

API
---

Check out the test.py file. It contains a basic usage example.

```python
from tvvenn import Tvvenn

tokens = [
  ('token_name', 'app_key', 'app_secret'),
]
query = '@someone.followers & @someother.friends' # your complex set operations here.
tvvenn = Tvvenn(tokens)
result = tvvenn.run(query) # returns an array of users ids
print tvvenn.hydrate(result) # returns a fully hydrated response
```

Available operations:

* AND, OR, XOR and the complement operators are built in.
* The possible options related to what set should be selected could be {followers, friends, all, ego, mutual}.

Minimal REST API
----------------

Start it with
```bash
python server.py
```
And go to `http://localhost:8000/`

The available get params are:
* query (string | mandatory)
* hydrated (boolean | optional)

e.g `http://localhost:8000/?query=@javierhonduco.followers`
