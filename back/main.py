import logging

from quart import Quart, request, jsonify
from quart_cors import cors
from telethon import TelegramClient
from telethon.sessions import StringSession

from settings import API_HASH, API_ID, SESSION_FILE

# get session information

try:
    with open(SESSION_FILE) as fh:
        session_string = fh.read()
        if not session_string:
            raise ValueError('Missing auth session string, run auth.py first')
except FileNotFoundError or Exception:
    logging.exception(f'when reading session file:')
    raise

app = Quart(__name__)
app = cors(app, allow_origin=["http://localhost:8080", "http://127.0.0.1:8080"])


def get_client() -> TelegramClient:
    return TelegramClient(StringSession(session_string), API_ID, API_HASH)


def parse_data(data) -> dict:
    restricted = ['access_hash', 'id', 'phone']
    return {k: v for k, v in data.__dict__.items()
            if isinstance(v, (int, str, bool, float))
            and k not in restricted}


@app.route('/me')
async def me():
    try:
        async with get_client() as client:
            data = await client.get_me()
            return parse_data(data)
    except Exception as e:
        logging.exception('when retrieving self info:')
        return {'error': f'{e}'}


@app.route('/info', methods=['POST'])
async def info():
    try:
        data = await request.get_json()
    except Exception as e:
        logging.exception(f'when decoding JSON')
        return {'error': f'{e}'}

    entity = data.get('entity')
    if not entity:
        return {'error': 'specify entity'}

    logging.debug(f'requested {entity} info')
    async with get_client() as client:
        data = await client.get_entity(entity)
        return parse_data(data)


@app.route('/check')
async def check():
    """simple healthcheck"""
    return {'status': 'ok'}


@app.route('/')
async def root():
    return f'it works'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
