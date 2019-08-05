import requests
from pprint import pprint

def api_test():
    r = requests.get('http://api.open-notify.org/astros.json')
    pprint(r)
