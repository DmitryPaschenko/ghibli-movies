from typing import List, Tuple, Dict
from movies.utils import ghibli_request
from movies.settings import Api
from movies.models import MovieModel
from movies.errors import BuildMovieListError


def fetch_movies(session) -> Tuple[str, List]:
    return ghibli_request(Api.MOVIES, session)


def fetch_people(session) -> Tuple[str, List]:
    return ghibli_request(Api.PEOPLE, session)


def build_movies_list(movies: List, people: List) -> List[Dict]:
    try:
        movie_people = {}
        for p in people:
            for movie in p.get("films", []):
                movie_id = movie.split('/')[-1]
                if movie_id in movie_people:
                    movie_people[movie_id].append(p)
                else:
                    movie_people[movie_id] = [p]
        built_movies = []
        for m in movies:
            built_movies.append(MovieModel.build(m, movie_people).serialize())

        return built_movies
    except Exception as e:
        raise BuildMovieListError(f'build movies list exception: "{e}"')
