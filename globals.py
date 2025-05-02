import os
from dotenv import load_dotenv

from enum import Enum

VERSION = '0.1'

DEFAULT_VERSION_ENDPOINT = '/api/version'

DEFAULT_API_PREFIX = '/api/v1'
DEFAULT_API_TITLE = 'LUCID ROUTES API'
DEFAULT_API_VERSION = ''
DEFAULT_SWAGGER_URL = '/api-docs'
DEFAULT_DEBUG = False
DEFAULT_PORT = 5000
DEFAULT_DEBUG_PATH = './debug'

#------------------------------

load_dotenv()

VERSION_ENDPOINT = os.getenv('VERSION_ENDPOINT', DEFAULT_VERSION_ENDPOINT)
API_PREFIX=os.getenv('API_PREFIX', DEFAULT_API_PREFIX)
API_TITLE=os.getenv('API_TITLE', DEFAULT_API_TITLE)
API_VERSION=os.getenv('API_VERSION', DEFAULT_API_VERSION)
SWAGGER_URL=os.getenv('SWAGGER_URL', DEFAULT_SWAGGER_URL)
DEBUG = os.getenv('FLASK_DEBUG', DEFAULT_DEBUG)
DEBUG = str(DEBUG).lower() in ['true', '1', 't', 'y', 'yes']
PORT = int(os.getenv('PORT', DEFAULT_PORT))
HOST_NAME = os.getenv('HOST_NAME', f'http://localhost:{PORT}')
DEBUG_PATH = os.getenv('DEBUG_PATH', DEFAULT_DEBUG_PATH)