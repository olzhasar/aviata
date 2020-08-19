import redis

from .settings import Settings

cache = redis.Redis(
    host=Settings.REDIS_HOST, port=Settings.REDIS_PORT, db=Settings.REDIS_DB
)
