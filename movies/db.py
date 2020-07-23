import json
from typing import List, Dict
from movies.utils import get_redis
from movies.settings import MOVIES_REDIS_KEY
from movies.errors import DBError
from movies.models import MovieModel


def save_movies(built_movies: List[Dict]):
    try:
        r = get_redis()
        return r.set(MOVIES_REDIS_KEY, json.dumps(built_movies))
    except Exception as e:
        raise DBError(f'save movies error: {e}')


def get_movies() -> List[MovieModel]:
    try:
        r = get_redis()
        data = r.get(MOVIES_REDIS_KEY)
        if data is None:
            return None

        data = json.loads(data)
        movies = []
        for movie_data in data:
            movies.append(MovieModel.deserialize(movie_data))

        return movies
    except Exception as e:
        raise DBError(f'get movies error: {e}')
