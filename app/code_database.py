import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

PANTRY_KEY = os.getenv('PANTRY_KEY')

# this is a bad idea but i kinda dont care since we are only using one
# pantry anyway
def basket_request(method='GET', payload='', basket=None):
    # basket names will always have "codes-" prefix
    # "codes" is the legacy basket
    BASKET_URL = f'https://getpantry.cloud/apiv1/pantry/{PANTRY_KEY}/basket/codes'

    if basket is not None:
        BASKET_URL += '-' + basket

    headers = {
        'Content-Type': 'application/json'
    }
    return requests.request(
        method=method, 
        url=BASKET_URL,
        headers=headers, 
        data=payload
    )


def get_basket(key=None, basket=None):
    print(f'[{basket} : {key}] Fetching pantry basket...')
    response = basket_request(method='GET', basket=basket)
    
    if not response:
        print(f'Empty basket: {basket}')
        return None
    
    data = json.loads(response.text)

    if key is None:
        return data

    try:
        return data[key]
    except KeyError:
        return None


def get_saved_codes(game=None):
    print(f'[{game}] Getting saved codes...')
    return get_basket(key='codes', basket=game)


def update_basket(data, basket=None):
    payload = json.dumps(data)
    basket_request(method='POST', payload=payload, basket=basket)


def update_saved_codes(codes, game=None):
    print(f'[{game}] Updating saved codes to pantry...')
    update_basket(
        data={
        'codes': codes
        }, basket=game
    )


if __name__ == '__main__':
    print('running as main')

    print(get_basket(key='ayaya', basket='some-game'))

    stuff = {'stuff': 'lmao'}
    update_basket(data=stuff, basket='some-game')

    print(get_basket(basket='some-game'))