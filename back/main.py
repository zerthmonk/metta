import os
import sys
import asyncio
import logging

from quart import Quart, request, jsonify
from quart_cors import cors

from client import SessionConfig, TeleGrabber
from settings import SESSION_FILE, SHARED, DEBUG, CORS_ORIGINS


app = Quart(__name__)
app = cors(app, allow_origin=CORS_ORIGINS)

grabber = TeleGrabber()
session = SessionConfig(SESSION_FILE)


async def get_json():
    try:
        await request.get_json()
    except Exception as e:
        logging.exception(f'when decoding JSON')
        return {'error': f'{e}'} 


@app.route('/me')
async def me():
    """get self info handle"""
    try:
        data = await grabber.get_info('me')
        return jsonify(data)
    except Exception as e:
        _msg = 'when retrieving self info:'
        logging.exception(_msg)
        return jsonify({'error': f'{_msg} {e}'})


@app.route('/info', methods=['POST'])
async def info():
    """get entity info handle"""
    data = await get_json()
    entity = data.get('entity')
    if not entity:
        return {'error': 'search item not specified!'}

    logging.debug(f'requested {entity} info')
    data = await grabber.get_info(entity)
    return jsonify(data)


@app.route('/channel')
async def get_channel_stat():
    """get channel statistics"""
    async with session.client.takeout(channels=True) as takeout:
        takeout.get_messages(target)
    return 'API check'


@app.route('/')
async def root():
    return 'it works'


async def new_session():
    authorized = await session.auth()
    client = await session.connect()
    return grabber.set_client(client)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(new_session())
    if session._session:
        app.run(host='0.0.0.0', debug=DEBUG)
    else:
        raise SystemExit('missing session string, user not authorized')
