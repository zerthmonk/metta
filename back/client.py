import logging
from telethon import TelegramClient
from telethon.sessions import StringSession

from auth import authenticate
from settings import API_HASH, API_ID, SESSION_FILE, SHARED, DEBUG, CORS_ORIGINS


class SessionConfig(object):

    def __init__(self, file_path):
        self.file_path = file_path
        self._session = ''
        self.client = None

    async def auth(self) -> str:
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

    def get_client(self) -> TelegramClient:
        if not self._session:
            raise SystemExit('client not authorized!')
        if not self.client:
            self.client = TelegramClient(StringSession(self._session), API_ID, API_HASH)
        return self.client

    async def connect(self):
        self.client = self.get_client()
        await self.client.connect()

    async def disconnect(self):
        await self.client.disconnect()


class TeleGrabber(object):
    """API methods collection"""

    client = None
    # I will remain silent and this info doesn't go anywhere
    restricted = [
        'access_hash', 
        'phone'
    ]

    def set_client(self, client: TelegramClient) -> TelegramClient:
        self.client = client
        return self.client

    def parse_data(self, payload) -> dict:
        """parse received from telegram"""
        data = payload.__dict__
        logging.debug(f'parsing {data}\n restricted fields: {self.restricted}')
        return {k: v for k, v in data.items()
                if isinstance(v, (int, str, bool, float))
                and k not in self.restricted}

    async def get_info(self, entity, with_photo=True) -> dict:
        """get full info from entity"""
        logging.debug(f'getting info for {entity}')
        async with self.client as client:
            data = await client.get_entity(entity)
            result = self.parse_data(data)
            if with_photo:
                image = await get_profile_photo(client, data)
                result.update({'photo': image})
            return result
    
    async def get_profile_photo(self, entity) -> str:
        """get photo by profile"""
        fpath = os.path.join(SHARED, f'{entity.id}.jpg')
        if os.path.isfile(fpath):
            return fpath
        logging.debug(f'downloading profile photo for {entity.id} to {fpath}')
        data = await self.client.download_profile_photo(entity, fpath)
        return fpath if data else ''

    async def get_takeout(self, entity, **kwargs)
        """take content with less limits
        
           support takeout named arguments
           https://docs.telethon.dev/en/latest/modules/client.html#telethon.client.account.AccountMethods
        """
        takeout_args = dict(groups=True, channels=True)
        if kwargs:
            takeout_args.update(**kwargs)
        logging.debug(f'taking out from channel {channel} with args: {takeout_args}')

        async with self.client.takeout() as takeout:
            takeout.get_messages(entity)
            data = {'info': 'messages received'}

            async for message in takeout.iter_messages(chat, wait_time=0):
                # here will be database ops
                # print(message.date)
                pass