import os, requests
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

def full_game_name(game: str) -> str:
    game_tag = {
        'genshin': 'Genshin Impact',
        'hkrpg': 'Honkai: Star Rail',
        'honkai3rd': 'Honkai Impact 3rd',
        'nap': 'Zenless Zone Zero',
        'tot': 'Tears of Themis',
        'wuwa': 'Wuthering Waves',
    }
    return game_tag.get(game, 'Other')


def webhook_username(game:str, type:str) -> str:
    username_fragment = {
        'new': 'New Codes',
        'active': 'Current Active Codes',
        'expired': 'Expired Codes',
    }

    selected_fragment = username_fragment.get(type, 'Unknown')
    selected_game_tag = full_game_name(game)

    return f'[{selected_game_tag}] {selected_fragment}'


def webhook_avatar(game:str) -> str:
    icon = {
        'genshin': 'https://play-lh.googleusercontent.com/iP2i_f23Z6I-5hoL2okPS4SxOGhj0q61Iyb0Y1m4xdTsbnaCmrjs7xKRnL6o5R4h-Yg=w240-h480-rw',
        'wuwa': 'https://play-lh.googleusercontent.com/ameFGPYH-qhOSxdsSA_fA54I4Ch-eO8y7Pj4x6W6ejQkvKbhVjCehKlPerBY9X2L8ek=w240-h480-rw',
        'hkrpg': 'https://play-lh.googleusercontent.com/cM6aszB0SawZNoAIPvtvy4xsfeFi5iXVBhZB57o-EGPWqE4pbyIUlKJzmdkH8hytuuQ',
        'nap': 'https://play-lh.googleusercontent.com/DEkjrvPufl6TG4Gxq4m8goCSLYiE1bLNOTnlKrJbHDOAWZT40qG3oyALMZJ2BPHJoe8',
        'honkai3rd': 'https://play-lh.googleusercontent.com/ci8QYc-jBQ_NC4dua2EQCGrcHtHFUnlfWctGMTnyTA4-Zu0gm6dJy382xxHp_TFhYg=w240-h480-rw',
    }
    
    return icon.get(game, None)


def webhook_thumbnail(game:str, type:str) -> str:
    thumb = {
        'genshin': {
            'new': 'https://static.wikia.nocookie.net/gensin-impact/images/5/55/Icon_Emoji_Paimon%27s_Paintings_01_Paimon_2.png/revision/latest?cb=20240303140740',
            'expired': 'https://static.wikia.nocookie.net/gensin-impact/images/f/f8/Icon_Emoji_Paimon%27s_Paintings_02_Qiqi_1.png/revision/latest/scale-to-width-down/1000?cb=20240303114539',
        },
        'wuwa' : {
            'new': 'https://wutheringlab.com/wp-content/uploads/T_ChatEmo_E_03.png',
            'expired': 'https://wutheringlab.com/wp-content/uploads/T_ChatEmo_D_03.png',
        }
    }

    selected_game = thumb.get(game, None)

    if selected_game is None:
        return None

    return selected_game.get(type, None)


def embed_maker(
        title: str = None,
        description: str = None,
        url: str = None,
        color: int = None,
        fields: list[dict] = None,
        author: dict = None,
        footer: dict = None,
        timestamp: str = None,
        image: dict = None,
        thumbnail: dict = None,
):
    if isinstance(author, str):
        author = {
            'name': author
        }
    
    if isinstance(footer, str):
        footer = {
            'text': footer
        }

    if isinstance(image, str):
        image = {
            'url': image
        }
    
    if isinstance(thumbnail, str):
        thumbnail = {
            'url': thumbnail
        }

    if fields is not None:
        fields = list(map(unify_field_type, fields))

    return {
        key: value for key, value in locals().items() if value is not None
    }


def unify_field_type(item):
    if isinstance(item, dict):
        # assume that the item is properly formatted
        # cant be bothered to bloat this func further
        return item

    if isinstance(item, (list, tuple)):
        if len(item) < 2:
            return { 'name': item[0], 'value': '' }
        else:
            return { 'name': item[0], 'value': item[1] }
    
    if isinstance(item, (str, int, float, bool)):
        return { 'name': str(item), 'value': '' }
    
    # dont error out, just return nothing if unsupported
    print('Unsupported item type on unify_field_type')
    return None


def send_webhook(
        content: str = None,
        embeds: list = [],
        username: str = None,
        avatar_url: str = None
):
    webhook_url = os.getenv('WEBHOOK_URL')

    if webhook_url is None:
        print('No webhook url found. Not sending anything.')
        return

    if isinstance(embeds, dict):
        embeds = [ embeds ]

    payload = {
        'username': username,
        'avatar_url': avatar_url,
        'embeds': embeds,
        'content': content,
    }

    response = requests.post(
        webhook_url,
        json=payload
    )

    if response.status_code == 204:
        print(f'Webhook sent. [[ {username} ]]')
    else:
        print(f'Failed to send webhook. Status code: {response.status_code}')


def send_new_codes(codes, game):
    if len(codes) < 1:
        print('No new codes. Sending nothing.')
        return
    
    ping_id = os.getenv('PING_ROLE_ID')

    embed = embed_maker(
        title='New codes!',
        author=full_game_name(game),
        fields=codes,
        color=16448000,
        timestamp=get_current_timestamp(),
        thumbnail=webhook_thumbnail(game, 'new'),
    )

    send_webhook(
        embeds=[embed],
        username=webhook_username(game, 'new'),
        avatar_url=webhook_avatar(game),
        content=f'Hey <@&{ping_id}>!',
    )


def send_expired_codes(codes, game):
    if len(codes) < 1:
        print('No expired codes. Sending nothing.')
        return

    expired_list = '\n'.join(codes)

    embed = embed_maker(
        title='Expired codes',
        author=full_game_name(game),
        description=f'The following have expired: \n```\n{expired_list}```',
        timestamp=get_current_timestamp(),
        thumbnail=webhook_thumbnail(game, 'expired'),
    )

    send_webhook(
        embeds=[embed],
        username=webhook_username(game,'expired'),
        avatar_url=webhook_avatar(game),
    )


def send_active_codes(codes):
    if len(codes) < 1:
        return

    pass


def get_current_timestamp():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'


if __name__ == '__main__':

    embed = embed_maker(
        title='Embed title',
        description='hello world from embed',
        author='embed author',
        footer='some footer',
        fields=[
            'string field',
            6969,
            ('single tuple'),
            ('tuple', 'tuple'),
            ['single item list'],
            ['pair list', 'value'],
            { 'name': 'proper', 'value': 'field' },
        ],
    )

    send_webhook(
        content='hello',
        embeds=[embed]
    )