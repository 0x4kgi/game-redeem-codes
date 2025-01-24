
import requests 

BASE_URL = 'https://hoyo-codes.seria.moe/codes?game='
VALID_GAMES = [
    'genshin', 'hkrpg', 'honkai3rd', 'nap', 'tot'
]

def fetch_codes(game='genshin'):
    if game not in VALID_GAMES:
        raise Exception(f'Game "{game}" is not valid. Must be one of the following: ' + ', '.join(VALID_GAMES))
    
    response = requests.get(BASE_URL + game)
    
    data = response.json()
    """
    {
        codes: [
            {
                id, code, status, game, rewards
            },
            ...
        ],
        game: string
    }
    """
    
    return data['codes']

def format_codes(codes):
    for item in codes:
        print(item['code'], ' - ', item['rewards'])

if __name__ == '__main__':
    
    genshin_codes = fetch_codes()
    hsr_codes = fetch_codes('hkrpg')
    zzz_codes = fetch_codes('nap')

    print('\ngenshin')
    print(format_codes(genshin_codes))

    print('\nhsr')
    print(format_codes(hsr_codes))

    print('\nzzz')
    print(format_codes(zzz_codes))