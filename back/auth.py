from telethon.sync import TelegramClient
from telethon.sessions import StringSession

from back.settings import API_HASH, API_ID


with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    """
        Keep this string safe! 
        Anyone with this string can use it to login into your account and do anything they want to to do.
    """
    with open('../.session', 'w') as fh:
        fh.write(client.session.save())
