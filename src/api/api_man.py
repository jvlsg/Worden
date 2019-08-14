import requests
from pprint import pprint

"""
Provides functions that call / parse / format data from the multiple apis
"""

def get_iss_position():
    """
    TEST function
    """
    try:
        r = requests.get('http://api.open-notify.org/iss-now.json')
        aux = r.json()
        return aux["iss_position"]
    except:
        return None