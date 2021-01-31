import os
import sys
import asyncio
import logging

from quart import Quart, request, jsonify
from quart_cors import cors
from telethon import TelegramClient
from telethon.sessions import StringSession

from auth import authenticate
from settings import API_HASH, API_ID, SESSION_FILE, SHARED, DEBUG


SESSION_STRING = ''
app = Quart(__name__)
app = cors(app, allow_origin=["http://localhost:8080", "http://127.0.0.1:8080"])


async def get_session_string(fpath):
    """read existing session string from file or try to authenticate"""
    try:
        with open(fpath) as fh:
            session_string = fh.read()
        if not session_string:
            session_string = await authenticate(fpath)
        return session_string
    except FileNotFoundError or Exception:
        logging.exception(f'when reading session file:')
        raise


def get_client() -> TelegramClient:
    return TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)


def parse_data(payload) -> dict:
    data = payload.__dict__
    restricted = ['access_hash', 'phone']
    logging.debug(f'parsing {data}\n restricted fields: {restricted}')
    return {k: v for k, v in data.items()
            if isinstance(v, (int, str, bool, float))
            and k not in restricted}


async def get_profile_photo(client, entity) -> str:
    fpath = os.path.join(SHARED, f'{entity.id}.jpg')
    if os.path.isfile(fpath):
        return fpath
    logging.debug(f'downloading profile photo for {entity.id} to {fpath}')
    data = await client.download_profile_photo(entity, fpath)
    return fpath if data else ''


async def get_info(entity, with_photo=True) -> dict:
    logging.debug(f'getting info for {entity}')
    async with get_client() as client:
        data = await client.get_entity(entity)
        result = parse_data(data)
        if with_photo:
            image = await get_profile_photo(client, data)
            result.update({'photo': image})
        return result


@app.route('/me')
async def me():
    try:
        data = await get_info('me')
        return data
    except Exception as e:
        _msg = 'when retrieving self info:'
        logging.exception(_msg)
        return {'error': f'{_msg} {e}'}


@app.route('/info', methods=['POST'])
async def info():
    try:
        data = await request.get_json()
    except Exception as e:
        logging.exception(f'when decoding JSON')
        return {'error': f'{e}'}

    entity = data.get('entity')
    if not entity:
        return {'error': 'search item not specified!'}

    logging.debug(f'requested {entity} info')
    data = await get_info(entity)
    return data


@app.route('/check')
async def check():
    """simple healthcheck"""
    return {'status': 'ok'}


@app.route('/')
async def root():
    return f'it works'


async def main():
    try:
        SESSION_STRING = await get_session_string(SESSION_FILE)
        return True
    except KeyboardInterrupt:
        await asyncio.sleep(0)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    authed = loop.run_until_complete(main())
    if authed:
        app.run(host='0.0.0.0', debug=DEBUG)
