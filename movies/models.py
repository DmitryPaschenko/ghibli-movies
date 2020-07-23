from typing import NamedTuple, List, Dict
from movies.errors import ModelError


class PeopleModel(NamedTuple):
    uid: str
    name: str

    @classmethod
    def build(cls, person: Dict):
        try:
            return cls(
                uid=person.get('id'),
                name=person.get('name')
            )
        except Exception as e:
            raise ModelError(f'people build error {e}. Data: {person}')

    @classmethod
    def deserialize(cls, data: Dict):
        try:
            return cls(
                uid=data.get('uid'),
                name=data.get('name')
            )
        except Exception as e:
            raise ModelError(f'people deserialize error {e}. Data: {data}')

    def serialize(self):
        try:
            return self._asdict()
        except Exception as e:
            raise ModelError(f'people serialize error {e}. Obj: {self}')


class MovieModel(NamedTuple):
    uid: str
    title: str
    description: str
    director: str
    producer: str
    release_date: str
    rt_score: str
    people: List[PeopleModel]

    @classmethod
    def build(cls, movie: Dict, people: Dict):
        try:
            clear_people = []
            for p in people.get(movie.get('id'), []):
                clear_people.append(PeopleModel.build(p))

            return cls(
                uid=movie.get('id'),
                title=movie.get('title'),
                description=movie.get('description'),
                director=movie.get('director'),
                producer=movie.get('producer'),
                release_date=movie.get('release_date'),
                rt_score=movie.get('rt_score'),
                people=clear_people
            )
        except Exception as e:
            raise ModelError(f'movie build error {e}. Data: {movie}, {people}')

    @classmethod
    def deserialize(cls, data: Dict):
        try:
            people = []
            for p in data.get('people', []):
                people.append(PeopleModel.deserialize(p))

            return cls(
                uid=data.get('uid'),
                title=data.get('title'),
                description=data.get('description'),
                director=data.get('director'),
                producer=data.get('producer'),
                release_date=data.get('release_date'),
                rt_score=data.get('rt_score'),
                people=people
            )
        except Exception as e:
            raise ModelError(f'movie deserialize error {e}. Data: {data}')

    def serialize(self):
        data = self._asdict()
        data.update({
            'people': [p.serialize() for p in self.people]
        })
        return data

    @property
    def people_list(self):
        people = []
        for p in self.people:
            people.append(p.name)

        return ', '.join(people) if people else '-'
