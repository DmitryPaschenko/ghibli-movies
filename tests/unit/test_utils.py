from unittest import TestCase
from unittest.mock import MagicMock
from redis import Redis
from movies.utils import get_redis, ghibli_request
from movies.settings import Api, REQUESTS_TIMEOUT
from movies.errors import GhibliRequestError


class UtilsTestCase(TestCase):
    def test_get_redis_instance(self):
        r = get_redis()
        self.assertIsInstance(r, Redis)

    def test_ghibli_request(self):
        session = MagicMock()
        api_name, data = ghibli_request(Api.MOVIES, session)
        session.get.assert_called_with(Api.MOVIES.value, timeout=REQUESTS_TIMEOUT)
        self.assertEqual(api_name, Api.MOVIES.name)

    def test_ghibli_request_error(self):
        session = MagicMock()
        session.get.side_effect = Exception('Test')
        with self.assertRaises(GhibliRequestError) as _:
            ghibli_request(Api.MOVIES, session)
