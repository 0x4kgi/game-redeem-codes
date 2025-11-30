import json
import sys

def get_json(basket):
    try:
        with open(f'codes/{basket}.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f'.json not found: codes/{basket}.json')
        return None
    
    return data


def save_json(payload='', basket=None):
    try:
        with open(f'codes/{basket}.json', 'w') as file:
            file.write(payload)
    except:
        print(f'Something went wrong with writing to codes/{basket}.json')


def get_basket(key=None, basket=None):
    print(f'[{basket} : {key}] Fetching pantry basket...')

    data = get_json(basket)
    
    if not data:
        print(f'Empty basket: {basket}')
        return None
    
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
    save_json(payload=payload, basket=basket)


def update_saved_codes(codes, game=None):
    print(f'[{game}] Updating saved codes to json...')
    update_basket(
        data={
        'codes': codes
        }, basket=game
    )


if __name__ == '__main__':
    args = sys.argv[1:]
    
    if len(args) < 1:
        n = get_json(None)
        c = get_json('c')
        
        print(n)
        print(c)
    elif args[0] == 'write-test' and args[1] is not None:
        print(f'writing to {args[1]}.json')
        update_basket({
            'key': 'value', 'some-key': 69, 'other': False
        }, args[1])
        print(get_basket(basket=args[1], key='other'))
    else:
        for arg in args:
            print(get_json(arg))