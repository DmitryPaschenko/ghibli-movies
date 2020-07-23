import json
from unittest import TestCase
from unittest.mock import patch
from movies.db import save_movies, get_movies
from movies.ghibli import build_movies_list
from movies.models import MovieModel
from movies.settings import MOVIES_REDIS_KEY
from movies.errors import DBError


class DBTestCase(TestCase):
    @patch('movies.db.get_redis')
    def test_save_movies(self, mock_get_redis):
        mock_redis = mock_get_redis.return_value
        built_movies = [{"id": 1}]
        save_movies(built_movies)
        mock_redis.set.assert_called_with(
            MOVIES_REDIS_KEY, json.dumps(built_movies))

    @patch('movies.db.get_redis')
    def test_save_movies_not_json_convertable(self, mock_get_redis):
        with self.assertRaises(DBError) as _:
            save_movies(object)

    @patch('movies.db.get_redis')
    def test_get_movies(self, mock_get_redis):
        mock_redis = mock_get_redis.return_value
        mock_redis.get.return_value = "[]"
        get_movies()
        mock_redis.get.assert_called_with(MOVIES_REDIS_KEY)

    @patch('movies.db.get_redis')
    def test_get_movies_no_data(self, mock_get_redis):
        mock_redis = mock_get_redis.return_value
        mock_redis.get.return_value = None
        res = get_movies()
        self.assertEqual(res, None)

    @patch('movies.db.get_redis')
    def test_get_movies_with_data(self, mock_get_redis):
        mock_redis = mock_get_redis.return_value

        with open(f'tests/data/movies.json', 'r') as f:
            movies = json.load(f)

        with open(f'tests/data/people.json', 'r') as f:
            people = json.load(f)
        movies_list = build_movies_list(movies, people)
        mock_redis.get.return_value = json.dumps(movies_list)
        res = get_movies()
        self.assertIsInstance(res[0], MovieModel)



