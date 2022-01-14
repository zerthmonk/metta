import logging
from settings import API_HASH, API_ID, SESSION_FILE

from telethon import TelegramClient
from telethon.sessions import StringSession


class SessionConfig:

    def __init__(self, file_path):
        self.file_path = file_path
        self._session = self._string_session()

    async def conn(self):
        if not self.client.is_connected():
            await self.client.connect()
        return self.client

    def _string_session(self):
        with open(SESSION_FILE) as fh:
            content = fh.read()
        return content

    @property
    def client(self) -> TelegramClient:
        if not self._session:
            raise SystemExit('not authorized!')
        return TelegramClient(StringSession(self._session), API_ID, API_HASH)
