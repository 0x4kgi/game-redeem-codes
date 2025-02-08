from .scraper import web_fetch
import requests 

HOYO_GAMES = [
    'genshin', 'hkrpg', 'honkai3rd', 'nap', 'tot'
]

def fetch_codes(game='genshin') -> list[dict[str, str]]:
    print('Attempting to fetch for ' + game)
    if game in HOYO_GAMES:
        return seria_fetch(game)
    elif game in ['wuwa']:
        return wuwa_fetch()
    else:
        raise Exception(f'Unknown game: {game}')


def seria_fetch(game='genshin') -> list[dict[str, str]]:
    print('Fetching from hoyo-codes.seria.moe/codes?game=' + game)
    if game not in HOYO_GAMES:
        raise Exception(f'Game "{game}" is not valid. Must be one of the following: ' + ', '.join(HOYO_GAMES))
    
    BASE_URL = 'https://hoyo-codes.seria.moe/codes?game='
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


def wuwa_fetch() -> list[dict[str, str]]:
    print('Finding codes for wuwa...')

    code_sources = [
        'https://www.pockettactics.com/wuthering-waves/codes',
        
        #'https://antifandom.com/wutheringwaves/wiki/Redemption_Code',        
        # lists different ones, for some reason?
        #'https://wuthering.gg/codes',
    ]
    
    codes = []
    
    for source in code_sources:
        codes += web_fetch.extract_codes(source)
    
    return codes


def format_codes(codes) -> None:
    # print('Formatting...')
    for item in codes:
        # print(item)
        print(item['code'], ' - ', item['rewards'])


if __name__ == '__main__':
    items = [
        ('genshin', fetch_codes('genshin')),
        ('hsr', fetch_codes('hkrpg')),
        ('zzz', fetch_codes('nap')),
        ('wuwa', fetch_codes('wuwa')),
    ]

    for item in items:
        print(f'\n{item[0]}')
        # print(item[1])
        print(format_codes(item[1]))
