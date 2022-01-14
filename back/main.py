import os
import time
import asyncio
import logging

from quart import Quart, request, jsonify
from quart_cors import cors

from session import SessionConfig
from settings import SESSION_FILE, SHARED, DEBUG, CORS_ORIGINS


app = Quart(__name__)
app = cors(app, allow_origin=CORS_ORIGINS)
session = SessionConfig(SESSION_FILE)


async def get_json():
    try:
        data = await request.get_json()
        return data
    except Exception as e:
        logging.exception(f'when decoding JSON')
        raise


async def get_info(entity, with_photo=True) -> dict:
    """get full info from entity"""
    logging.debug(f'getting info for {entity}')
    async with session.client as client:
        client.connect()
        data = await client.get_entity(entity)
        result = parse_data(data)
        if with_photo:
            image = await get_profile_photo(client, data)
            result.update({'photo': image})
        logging.debug(f'finished with result: {result}')
        return result


def parse_data(payload) -> dict:
    """parse received from telegram"""
    data = payload.__dict__
    restricted = ['access_hash', 'phone']
    logging.debug(f'parsing data with restricted fields: {restricted}')
    return {k: v for k, v in data.items()
            if isinstance(v, (int, str, bool, float))
            and k not in restricted}


async def get_profile_photo(client, entity) -> str:
    """get photo by profile"""
    fpath = os.path.join(SHARED, f'{entity.id}.jpg')
    if os.path.isfile(fpath):
        return fpath
    logging.debug(f'downloading profile photo for {entity.id} to {fpath}')
    data = await client.download_profile_photo(entity, fpath)
    return fpath if data else ''


async def get_takeout(entity, **kwargs):
    """take content with less limits

       support takeout named arguments
       https://docs.telethon.dev/en/latest/modules/client.html#telethon.client.account.AccountMethods
    """
    result = []
    takeout_args = dict(groups=True, channels=True)
    if kwargs:
        takeout_args.update(**kwargs)
    logging.debug(f'taking out from channel {entity} with args: {takeout_args}')

    # TODO: strange connection behavior, investigate
    async with session.client as client:
        async with client.takeout() as takeout:
            takeout.get_messages(entity)
            data = {'info': 'messages received'}
            async for message in takeout.iter_messages(entity, wait_time=0):
                # here will be database ops
                result.append(message.date)
    return result


@app.route('/api/me')
async def me():
    """get self info handle"""
    try:
        result = await get_info('me')
    except Exception as e:
        _msg = 'when retrieving self info:'
        logging.exception(_msg)
        result = {'error': f'{_msg} {e}'}
    return jsonify(result)


@app.route('/api/info', methods=['POST'])
async def info():
    """get entity info handle"""
    try:
        data = await get_json()
        entity = data.get('entity')
        if not entity:
            raise ValueError('entity name not specified!')
        logging.debug(f'requested {entity} info')
        result = await get_info(entity)
    except Exception as e:
        logging.exception('on /info endpoint: ')
        result = {'error': f'{e}'}
    return jsonify(result)


@app.route('/api/messages', methods=['POST'])
async def messages():
    """simple check"""
    try:
        data = await get_json()
        entity = data.get('entity')
        if not entity:
            raise ValueError('entity name not specified!')
        result = await get_takeout(entity)
    except Exception as e:
        logging.exception('on /messages endpoint: ')
        result = {'error': f'{e}'}
    return jsonify(result)


@app.route('/')
async def root():
    return 'it works'


if __name__ == '__main__':
    host = '0.0.0.0'
    if session.client:
        app.run(host=host, debug=DEBUG)
    else:
        raise SystemExit('run pipenv run auth.py first!')
