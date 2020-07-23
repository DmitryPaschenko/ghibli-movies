import logging


log = logging.getLogger(__name__)


class BaseError(Exception):
    def __init__(self, message, *args, **kwargs):
        log.error(message)
        super().__init__(message, *args, **kwargs)


class GhibliRequestError(BaseError):
    def __init__(self, message, *args, **kwargs):
        super().__init__('Ghibli Request Error: ' + message, *args, **kwargs)


class BuildMovieListError(BaseError):
    def __init__(self, message, *args, **kwargs):
        super().__init__('Build Movie List Error: ' + message, *args, **kwargs)


class DBError(BaseError):
    def __init__(self, message, *args, **kwargs):
        super().__init__('DB Error: ' + message, *args, **kwargs)


class ModelError(BaseError):
    def __init__(self, message, *args, **kwargs):
        super().__init__('Model Error: ' + message, *args, **kwargs)
