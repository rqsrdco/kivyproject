from os import environ, path

from dotenv import load_dotenv

# Load variables from .env
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

DEBUG = bool(environ.get('DEBUG', True))  # environ['DEBUG'] == 'True'
ENGINE_URL = environ.get('SQLITE')
CLEANUP_DATA = environ.get('CLEANUP_DATA')
PRODUCT_PHOTO_PATH = environ.get('PRODUCT_PHOTO_PATH')
