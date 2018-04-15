'''Run with PyTest'''

import requests
import pytest

# local_endpoint = "http://127.0.0.1:5000/"
local_endpoint = "https://dataframe.herokuapp.com/"
compare_endpoint = local_endpoint + 'compare'

def process_response(response):
    r_text = response.text
    try:
        response.raise_for_status()
        return r_text
    except:
        raise BaseException(r_text)

def test_compare():
    dfA = dict(key1='old', key2='older', key3='oldest')
    dfB = dict(key1='new', key2='newer', key3='newest')
    dfOld = dict(keyA=dfA, keyB=dfA)
    dfNew = dict(keyA=dfB, keyC=dfB)
    r = requests.post(compare_endpoint, json=dict(old=dfOld, new=dfNew), headers=dict(Authorization='token'))
    response = process_response(r)
    print(response)