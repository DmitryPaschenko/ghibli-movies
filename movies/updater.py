import asyncio
from concurrent.futures import ThreadPoolExecutor

import requests
from movies.settings import Api
from movies.db import save_movies
from movies.ghibli import fetch_people, fetch_movies, build_movies_list


async def _collect_movie_list():
    with ThreadPoolExecutor(max_workers=10) as executor:
        with requests.Session() as session:
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(
                    executor,
                    fetch_movies,
                    *(session,)
                ),
                loop.run_in_executor(
                    executor,
                    fetch_people,
                    *(session,)
                )
            ]

            movies = []
            people = []
            for api_name, data in await asyncio.gather(*tasks):
                if api_name == Api.MOVIES.name:
                    movies = data
                elif api_name == Api.PEOPLE.name:
                    people = data

            built_movies = build_movies_list(movies, people)
            save_movies(built_movies)


def update_movie_list():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future = asyncio.ensure_future(_collect_movie_list())
    loop.run_until_complete(future)
