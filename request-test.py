import requests
from pprint import pprint

r = requests.get('http://api.open-notify.org/astros.json')
pprint(r)
