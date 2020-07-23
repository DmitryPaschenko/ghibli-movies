import os
import enum


REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', 'sOmE_sEcUrE_pAsS')
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')
MOVIES_REDIS_KEY = os.getenv('MOVIES_REDIS_KEY', 'films123')
CELERY_BROKER_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0'
REQUESTS_TIMEOUT = 30
UPDATE_PERIOD = 60


class Api(enum.Enum):
    MOVIES = 'https://ghibliapi.herokuapp.com/films?limit=250'
    PEOPLE = 'https://ghibliapi.herokuapp.com/people?' \
             'limit=250&fields=id,name,films'
