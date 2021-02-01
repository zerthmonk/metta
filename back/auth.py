import sys
import asyncio
import logging

from telethon import TelegramClient
from telethon.sessions import StringSession

from settings import API_HASH, API_ID, SESSION_FILE


async def authenticate(fpath):
    """Authenticate in Telegram and save string to .session file

        Keep this string safe!
        Anyone with this string can use it to login into your account and do anything they want to to do.
    """
    try:
        if __name__ != '__main__':
            logging.warning('First run for authentication should be: `docker-compose run --rm <backend-name>` '\
                            'Do not run it with `docker-compose up` without authentication. It will hang.')

        async with TelegramClient(StringSession(), API_ID, API_HASH) as client:
            with open(fpath, 'w') as fh:
                session_string = client.session.save()
                fh.write(session_string)
                return session_string
    except KeyboardInterrupt:
        print('\n')
        logging.debug('input terminated by user')
        await asyncio.sleep(0)
        sys.exit(0)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(authenticate(SESSION_FILE))
