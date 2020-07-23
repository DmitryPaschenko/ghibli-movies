import requests
import json
from unittest import TestCase
from unittest.mock import patch
from movies.ghibli import fetch_movies, fetch_people, build_movies_list
from movies.settings import Api


class FetchDataTestCase(TestCase):
    @patch('movies.ghibli.ghibli_request')
    def test_fetch_movies(self, mock_ghibli_request):
        with requests.Session() as session:
            fetch_movies(session)
            mock_ghibli_request.assert_called_with(Api.MOVIES, session)

    @patch('movies.ghibli.ghibli_request')
    def test_fetch_people(self, mock_ghibli_request):
        with requests.Session() as session:
            fetch_people(session)
            mock_ghibli_request.assert_called_with(Api.PEOPLE, session)

    def test_build_movies_list_with_people(self):
        with open(f'tests/data/movies.json', 'r') as f:
            movies = json.load(f)

        with open(f'tests/data/people.json', 'r') as f:
            people = json.load(f)
        movies_list = build_movies_list(movies, people)
        self.assertEqual(len(movies_list[0].get('people', [])), 2)

    def test_build_movies_list_without_people(self):
        with open(f'tests/data/movies1.json', 'r') as f:
            movies = json.load(f)

        with open(f'tests/data/people.json', 'r') as f:
            people = json.load(f)
        movies_list = build_movies_list(movies, people)
        self.assertEqual(len(movies_list[0].get('people', [])), 0)

    def test_build_movies_list_no_movies(self):
        movies = []
        with open(f'tests/data/people.json', 'r') as f:
            people = json.load(f)
        movies_list = build_movies_list(movies, people)
        self.assertEqual(len(movies_list), 0)

    def test_build_movies_list_no_people(self):
        with open(f'tests/data/movies.json', 'r') as f:
            movies = json.load(f)
        people = []
        movies_list = build_movies_list(movies, people)
        self.assertEqual(len(movies_list), 1)
