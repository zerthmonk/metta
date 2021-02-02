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


async def new_session():
    authorized = await session.auth()
    client = await session.connect()
    return grabber.set_client(client)


async def get_json():
    try:
        await request.get_json()
    except Exception as e:
        logging.exception(f'when decoding JSON')
        raise


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
    try:
        data = await get_json()
        entity = data.get('entity')
        if not entity:
            raise ValueError('search item is missing in request data')
    except ValueError or Exception:
        data = {'error': f'{e}'}
    else:
        logging.debug(f'requested {entity} info')
        data = await grabber.get_info(entity)
    return jsonify(data)


@app.route('/channel')
async def get_channel_stat():
    """get channel statistics"""
    try:
        data = await.get_json()
        channel = data.get('channel')
        if not channel:
            raise ValueError('target channel name is missing')
    except ValueError or Exception:
        data = {'error': f'{e}'}
    else:
        logging.debug(f'taking out messages from channel {channel}')
        async with session.client.takeout(channels=True) as takeout:
            takeout.get_messages(target)
            data = {'info': 'messages received'}
    return jsonify(data)


@app.route('/healthcheck')
async def healthcheck()
    """simple healthcheck"""
    state = 'not connected'
    if session.client.is_connected():
        state = 'connected'
    return f'client {state}'


@app.route('/')
async def root():
    return 'it works'


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(new_session())
    if session.client.is_connected():
        app.run(host='0.0.0.0', debug=DEBUG)
    else:
        raise SystemExit('client not connected')
