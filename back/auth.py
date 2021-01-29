from telethon.sync import TelegramClient
from telethon.sessions import StringSession

from settings import API_HASH, API_ID, SESSION_FILE


with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    """
        Keep this string safe! 
        Anyone with this string can use it to login into your account and do anything they want to to do.
    """
    with open(SESSION_FILE, 'w') as fh:
        fh.write(client.session.save())
