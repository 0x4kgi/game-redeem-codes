import json
import sys
from app.code_fetch     import fetch_codes
from app.code_database  import get_saved_codes, update_saved_codes
from app.send_webhook   import send_new_codes, send_expired_codes


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

    new_codes = []
    for item in codes['live']:
        _c = item[0]
        if _c in code_status_group['new']:
            new_codes.append(item)

    return {
        'new': new_codes,
        'active': active,
        'expired': code_status_group['expired'],
    }


def grab_live_codes(game='genshin'):
    codes = [
        (i['code'], i['rewards']) 
            for i in fetch_codes(game)
    ]

    db_codes = get_saved_codes(game)

    # if not None does not work, idk why
    if not db_codes:
        db_codes = []
    
    return {
        'live': codes,
        'saved': db_codes
    }


def main(game, test_mode):
    print(f'[{game}] Running main process')
    
    codes = grab_live_codes(game)
    
    # main "process"
    print(json.dumps(codes, indent=2))
    processed_codes = process_codes(codes)

    # end of function, print or save
    if test_mode:
        print(f'[{game}] Test done! The following are the processed data:')
        print(json.dumps(processed_codes, indent=2))

        status_map = {
            'active': f'[{game}] saved to db',
            'new': f'[{game}] sent as new webhook',
            'expired': f'[{game}] sent as expired webhook',
        }

        for status, message in status_map.items():
            print(f'\n{message}')
            print(json.dumps(processed_codes[status], indent=2))
    else:
        print(f'[{game}] Processing done! Attempting to save and send webhooks.')

        update_saved_codes(
            codes=processed_codes['active'], game=game
        )
        send_new_codes(
            codes=processed_codes['new'], game=game
        )
        send_expired_codes(
            codes=processed_codes['expired'], game=game
        )


if __name__ == '__main__':
    # for testing, append anything to the script
    # it will automatically be on "test mode"
    test_mode = len(sys.argv) > 1

    main('genshin', test_mode)
    main('wuwa', test_mode)