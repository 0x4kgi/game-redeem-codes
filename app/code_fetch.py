
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

genshin_codes = fetch_codes()
hsr_codes = fetch_codes('hkrpg')
zzz_codes = fetch_codes('nap')