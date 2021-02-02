import asyncio
import logging

from auth import authenticate
from settings import API_HASH, API_ID

from telethon import TelegramClient
from telethon.sessions import StringSession


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
        client = TelegramClient(StringSession(self._session), API_ID, API_HASH)
        client.connect()
        return client
