import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

PANTRY_KEY = os.getenv('PANTRY_KEY')
BASKET_URL = f'https://getpantry.cloud/apiv1/pantry/{PANTRY_KEY}/basket/codes'

# this is a bad idea but i kinda dont care since we are only using one
# pantry anyway
def basket_request(method='GET', payload=''):
    headers = {
        'Content-Type': 'application/json'
    }
    return requests.request(
        method=method, 
        url=BASKET_URL,
        headers=headers, 
        data=payload
    )


def get_basket(key=None):
    response = basket_request('GET')
    data = json.loads(response.text)

    if key is None:
        return data

    try:
        return data[key]
    except KeyError:
        return None


def get_saved_codes():
    return get_basket('codes')


def update_basket(data):
    payload = json.dumps(data)
    basket_request('POST', payload)


def update_saved_codes(codes):
    update_basket({
        'codes': codes
    })


if __name__ == '__main__':
    print('running as main')

    print(get_basket('ayaya'))

    stuff = {'stuff': 'lmao'}
    update_basket(stuff)

    print(get_basket())