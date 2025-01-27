import json
from app.code_fetch     import fetch_codes
from app.code_database  import get_saved_codes, update_saved_codes
from app.send_webhook   import send_new_codes, send_expired_codes

import sys

codes = [
    (i['code'], i['rewards']) for i in fetch_codes('genshin')
]

db_codes = get_saved_codes()


def compare_codes(fetched, saved):
    fetched_just_codes = [i[0] for i in fetched]

    set_fetched = set(fetched_just_codes)
    set_saved   = set(saved)

    common  = list(set_fetched & set_saved)
    new     = list(set_fetched - set_saved)
    expired = list(set_saved - set_fetched)

    return {
        'new'       : new,
        'active'    : common,
        'expired'   : expired,
    }


def process_codes(codes):
    code_status_group = compare_codes(codes['live'], codes['saved'])
    
    active = code_status_group['active'] + code_status_group['new']

    update_saved_codes(active)

    new_codes = []
    for item in codes['live']:
        _c = item[0]
        if _c in code_status_group['new']:
            new_codes.append(item)

    send_new_codes(new_codes)
    send_expired_codes(code_status_group['expired'])


def grab_live_codes(game='genshin'):
    codes = [
        (i['code'], i['rewards']) 
            for i in fetch_codes(game)
    ]

    db_codes = get_saved_codes()
    
    return {
        'live': codes,
        'saved': db_codes
    }


if __name__ == '__main__':
    # for testing, append anything to the script
    # it will automatically be on "test mode"
    args = sys.argv
    
    if len(args) > 1:
        codes = {
            'live': [
                ('c1', 'first code'),
                ('c2', 'second code'),
                ('c3', 'third code'),
                ('new', 'this is new'),
                ('new2', 'so this one!'),
                ('new3', 'me three!!'),
            ],
            'saved': [
                'c1','c2','c3',
                'expired',
                'another expired',
                'something else expired'
            ],
        }
    else:
        codes = grab_live_codes('genshin')
    
    print(json.dumps(codes, indent=2))
    process_codes(codes)