import os
import logging
from dotenv import load_dotenv
from back.logger import get_logger

load_dotenv()

DEBUG = os.getenv('DEBUG')
ROOT = os.path.dirname(os.path.dirname(__file__))

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

HOST = os.getenv('HOST', '127.0.0.1')
PORT = os.getenv('PORT', 5000)

SESSION_FILE = os.path.join(ROOT, '.session')

logging.root = get_logger(ROOT, DEBUG)

if not API_HASH or not API_ID:
    raise SystemExit('API_ID/API_HASH pair not set, check .env file')

if DEBUG:
    logging.debug('[!] DEBUG ENABLED')

if not os.path.exists(SESSION_FILE):
    with open(SESSION_FILE, 'w') as fh:
        fh.write('')