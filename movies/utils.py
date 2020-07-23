from typing import List, Tuple
from redis import Redis
from requests.sessions import Session
from movies.errors import GhibliRequestError
from movies.settings import (
    Api, REQUESTS_TIMEOUT, REDIS_HOST, REDIS_PASSWORD, REDIS_PORT
)


def ghibli_request(api: Api, session: Session) -> Tuple[str, List]:
    try:
        with session.get(api.value, timeout=REQUESTS_TIMEOUT) as response:
            data = response.json()
            response.raise_for_status()
            return api.name, data
    except Exception as e:
        raise GhibliRequestError(
            f'Fetch data error. Url: "{api.value}". Exc: {e}')


def get_redis() -> Redis:
    return Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
