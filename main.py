from app.code_fetch     import fetch_codes
from app.code_database  import get_saved_codes, update_saved_codes
from app.send_webhook   import send_new_codes, send_expired_codes

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


code_status_group = compare_codes(codes, db_codes)
active = code_status_group['active'] + code_status_group['new']

update_saved_codes(active)

new_codes = []
for item in codes:
    _c = item[0]
    if _c in code_status_group['new']:
        new_codes.append(item)

send_new_codes(new_codes)
send_expired_codes(code_status_group['expired'])