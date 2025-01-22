from app.code_fetch import genshin_codes

for item in genshin_codes:
    print(item['code'], '\t', item['rewards'])