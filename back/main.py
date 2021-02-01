import os
import sys
import asyncio
import logging

from quart import Quart, request, jsonify
from quart_cors import cors
from telethon import TelegramClient
from telethon.sessions import StringSession

from auth import authenticate
from settings import API_HASH, API_ID, SESSION_FILE, SHARED, DEBUG, CORS_ORIGINS


SESSION_STRING = ''
app = Quart(__name__)
app = cors(app, allow_origin=CORS_ORIGINS)


class SessionConfig:

    def __init__(self, file_path):
        self.file_path = file_path
        self._session = ''

    async def auth(self):
        """read existing session string from file or try to authenticate"""
        if self._session:
            return self._session

        try:
            with open(self.file_path) as fh:
                self._session = fh.read()
            if not self._session:
                self._session = await authenticate(self.file_path)
            return self._session
        except KeyboardInterrupt:
            await asyncio.sleep(0)
        except FileNotFoundError or Exception:
            logging.exception(f'when reading session file:')
            raise

    @property
    def client(self) -> TelegramClient:
        if not self._session:
            raise SystemExit('not authorized!')
        return TelegramClient(StringSession(self._session), API_ID, API_HASH)


session = SessionConfig(SESSION_FILE)


async def get_info(entity, with_photo=True) -> dict:
    """get full info from entity"""
    logging.debug(f'getting info for {entity}')
    async with session.client as client:
        data = await client.get_entity(entity)
        result = parse_data(data)
        if with_photo:
            image = await get_profile_photo(client, data)
            result.update({'photo': image})
        return result


def parse_data(payload) -> dict:
    """parse received from telegram"""
    data = payload.__dict__
    restricted = ['access_hash', 'phone']
    logging.debug(f'parsing {data}\n restricted fields: {restricted}')
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


@app.route('/me')
async def me():
    """get self info handle"""
    try:
        data = await get_info('me')
        return jsonify(data)
    except Exception as e:
        _msg = 'when retrieving self info:'
        logging.exception(_msg)
        return jsonify({'error': f'{_msg} {e}'})


@app.route('/info', methods=['POST'])
async def info():
    """get entity info handle"""
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
    return jsonify(data)


@app.route('/check')
async def check():
    """simple check"""
    return 'API check'

@app.route('/')
async def root():
    return 'it works'


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(session.auth())
    if session._session:
        app.run(host='0.0.0.0', debug=DEBUG)
    else:
        raise SystemExit('missing session string, user not authorized')
