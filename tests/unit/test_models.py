import json
from unittest import TestCase
from movies.models import MovieModel, PeopleModel
from movies.errors import ModelError


class PeopleModelTestCase(TestCase):
    def setUp(self):
        with open(f'tests/data/person.json', 'r') as f:
            person = json.load(f)

        self.p_model = PeopleModel.build(person)

    def test_build_people_model(self):
        self.assertIsInstance(self.p_model, PeopleModel)

    def test_build_people_values(self):
        self.assertEqual(
            self.p_model.uid, 'ba924631-068e-4436-b6de-f3283fa848f0')
        self.assertEqual(self.p_model.name, 'Ashitaka')

    def test_build_people_error(self):
        with self.assertRaises(ModelError) as _:
            PeopleModel.build(None)

    def test_serialize_dict(self):
        data = self.p_model.serialize()
        self.assertIsInstance(data, dict)

    def test_serialize_values(self):
        data = self.p_model.serialize()
        self.assertEqual(self.p_model.uid, data.get('uid'))
        self.assertEqual(self.p_model.name, data.get('name'))

    def test_deserialize(self):
        deserialized = PeopleModel.deserialize(self.p_model.serialize())
        self.assertEqual(self.p_model, deserialized)

    def test_deserialize_error(self):
        with self.assertRaises(ModelError) as _:
            PeopleModel.deserialize(None)


class MovieModelTestCase(TestCase):
    def setUp(self):
        with open(f'tests/data/movie.json', 'r') as f:
            movie = json.load(f)

        with open(f'tests/data/movie_people.json', 'r') as f:
            movie_people = json.load(f)

        self.m_model = MovieModel.build(movie, movie_people)

    def test_build_movie_model(self):
        self.assertIsInstance(self.m_model, MovieModel)
        self.assertIsInstance(self.m_model.people[0], PeopleModel)

    def test_build_movie_values(self):
        self.assertEqual(
            self.m_model.uid, '2baf70d1-42bb-4437-b551-e5fed5a87abe')
        self.assertEqual(self.m_model.title, 'Castle in the Sky')
        self.assertEqual(self.m_model.description, 'The orphan Sheeta inherited')
        self.assertEqual(self.m_model.director, 'Hayao Miyazaki')
        self.assertEqual(self.m_model.producer, 'Isao Takahata')
        self.assertEqual(self.m_model.release_date, '1986')
        self.assertEqual(self.m_model.rt_score, '95')
        self.assertEqual(len(self.m_model.people), 2)

    def test_build_movie_error(self):
        with self.assertRaises(ModelError) as _:
            MovieModel.build(None, None)

    def test_serialize_dict(self):
        data = self.m_model.serialize()
        self.assertIsInstance(data, dict)

    def test_serialize_values(self):
        data = self.m_model.serialize()
        self.assertEqual(self.m_model.uid, data.get('uid'))
        self.assertEqual(self.m_model.title, data.get('title'))
        self.assertEqual(self.m_model.description, data.get('description'))
        self.assertEqual(self.m_model.director, data.get('director'))
        self.assertEqual(self.m_model.producer, data.get('producer'))
        self.assertEqual(self.m_model.release_date, data.get('release_date'))
        self.assertEqual(self.m_model.rt_score, data.get('rt_score'))
        self.assertEqual(len(self.m_model.people), len(data.get('people')))

    def test_deserialize(self):
        deserialized = MovieModel.deserialize(self.m_model.serialize())
        self.assertEqual(self.m_model, deserialized)

    def test_deserialize_error(self):
        with self.assertRaises(ModelError) as _:
            MovieModel.deserialize(None)
