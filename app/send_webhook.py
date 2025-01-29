import os, requests
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

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


def send_new_codes(codes):
    if len(codes) < 1:
        print('No new codes. Sending nothing.')
        return
    
    ping_id = os.getenv('PING_ROLE_ID')

    embed = embed_maker(
        title='New codes!',
        fields=codes,
        color=16448000,
        timestamp=get_current_timestamp(),
        thumbnail='https://static.wikia.nocookie.net/gensin-impact/images/5/55/Icon_Emoji_Paimon%27s_Paintings_01_Paimon_2.png/revision/latest?cb=20240303140740',
    )

    send_webhook(
        embeds=[embed],
        username='New!',
        content=f'Hey <@&{ping_id}>!',
    )


def send_expired_codes(codes):
    if len(codes) < 1:
        print('No expired codes. Sending nothing.')
        return

    expired_list = '\n'.join(codes)

    embed = embed_maker(
        title='Expired codes',
        description=f'The following have expired: \n```\n{expired_list}```',
        timestamp=get_current_timestamp(),
        thumbnail='https://static.wikia.nocookie.net/gensin-impact/images/f/f8/Icon_Emoji_Paimon%27s_Paintings_02_Qiqi_1.png/revision/latest/scale-to-width-down/1000?cb=20240303114539',
    )

    send_webhook(embeds=[embed],username='Expired')


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