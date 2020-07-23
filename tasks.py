from __future__ import absolute_import, unicode_literals
import logging
from celery import Celery
from movies.updater import update_movie_list
from movies.settings import CELERY_BROKER_URL, UPDATE_PERIOD


log = logging.getLogger('tasks')
app = Celery('tasks', broker=CELERY_BROKER_URL)


@app.task(time_limit=UPDATE_PERIOD)
def update_movies():
    log.info('Update movies start')
    update_movie_list()
    log.info('Update movies end')


app.conf.beat_schedule = {
    'update_movies': {
        'task': 'tasks.update_movies',  # instead 'show'
        'schedule': UPDATE_PERIOD
    }
}
app.conf.timezone = 'UTC'
