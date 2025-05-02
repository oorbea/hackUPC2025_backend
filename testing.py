"""
Testing environment configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
VERSION_ENDPOINT = '/api/version'
API_PREFIX = '/api/v1'
API_TITLE = 'LUCID ROUTES API (TEST)'
API_VERSION = 'test'
SWAGGER_URL = '/api-docs'
DEBUG = False
PORT = 5000
HOST_NAME = f'http://localhost:{PORT}'

TESTING = True