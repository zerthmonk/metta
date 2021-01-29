import logging

from quart import Quart, request, jsonify
from telethon import TelegramClient
from telethon.sessions import StringSession

from back.settings import API_HASH, API_ID, SESSION_FILE

app = Quart(__name__)


def parse_data(data):
    requested = [
        'name',
        'username',
    ]
    return {k: v for k, v in data.items() if k in requested}


def get_client() -> TelegramClient:
    try:
        with open(SESSION_FILE) as fh:
            session_string = fh.read()
            if not session_string:
                raise ValueError('Missing auth session string, run auth.py first')
    except FileNotFoundError or Exception:
        logging.exception(f'when reading session file:')
        raise
    else:
        return TelegramClient(StringSession(session_string), API_ID, API_HASH)


@app.route('/info', methods=['POST'])
async def info():
    data = await request.form
    entity = data.get('entity')
    if not entity:
        return jsonify({'error': 'specify entity'})
    logging.debug(f'requested {entity} info')
    async with get_client() as client:
        data = await client.get_entity(entity)
        return jsonify(parse_data(data.__dict__))


@app.route('/')
async def root():
    return f'it works'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
