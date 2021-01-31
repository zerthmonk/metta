import os
import logging
from dotenv import load_dotenv
from logger import get_logger

DEBUG = os.getenv('DEBUG')

if os.getenv('DOCKER'):
      # variables set in docker-compose.yml or .env file
    SHARED = os.getenv('SHARED')
    SESSION = os.getenv('SESSION')
    SESSION_FILE = os.path.join(SESSION, '.session')
    logging.root = get_logger(SESSION, DEBUG)
    # cors wildcard because of docker trickery
else:
    load_dotenv()
    APPROOT = os.path.dirname(os.path.dirname(__file__))
    # sharing files with front (fast and dirty way)
    SHARED = os.path.join(APPROOT, 'files', 'shared')
    # Telegram session store
    SESSION_FILE = os.path.join(APPROOT, 'files', 'session', '.session')
    # set logging
    logging.root = get_logger(APPROOT, DEBUG)

# Telegram credentials
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
# Quart params
HOST = os.getenv('HOST', '127.0.0.1')
PORT = os.getenv('PORT', 5000)

CORS_ORIGINS = [
  'http://localhost:8080',
  'http://127.0.0.1:8080',
  'http://metta-proxy',
  'http://metta-front'
]


if not API_HASH or not API_ID:
    raise SystemExit('API_ID/API_HASH pair not set, check .env file')

if DEBUG:
    logging.debug('[!] DEBUG ENABLED')

if not os.path.exists(SESSION_FILE):
    with open(SESSION_FILE, 'w') as fh:
        fh.write('')
