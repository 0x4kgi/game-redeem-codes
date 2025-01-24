from app.code_fetch     import fetch_codes
from app.code_database  import get_saved_codes, update_saved_codes

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

# print(compare_codes(codes, db_codes))

code_status_group = compare_codes(codes, db_codes)

print(code_status_group)

active = code_status_group['active'] + code_status_group['new']

print(active)

update_saved_codes(active)