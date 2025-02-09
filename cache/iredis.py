import pickle
from typing import Any
from flask.cli import F
from matplotlib.pylab import f
import redis
from config import db_config
import json


class RedisPool:
    instance = None

    def __init__(self):
        self.pool = redis.ConnectionPool(
            host=db_config.REDIS_DB_HOST,
            port=db_config.REDIS_DB_PORT,
            db=db_config.REDIS_DB_NUM,
            password=db_config.REDIS_DB_PWD,
            decode_responses=True,
            max_connections=10)

    def __getConnection(self):
        conn = redis.Redis(connection_pool=self.pool)
        return conn

    @classmethod
    def getConn(cls):
        if RedisPool.instance is None:
            RedisPool.instance = RedisPool()
        return RedisPool.instance.__getConnection()


def pop_crawler_task(type) -> Any:
    task = RedisPool().getConn().lpop('crawler_task_' + type)
    if task:
        return json.loads(task)
    return None


def push_crawler_task(type, task):
    serialized_task = json.dumps(task)
    RedisPool().getConn().rpush('crawler_task_' + type, serialized_task)


def update_cookie(platform, user_id, cookie):
    RedisPool().getConn().setex(f'cookie_{platform}_{user_id}', 24 * 60 * 60, cookie)


def get_cookie(platform, user_id):
    return RedisPool().getConn().get(f'cookie_{platform}_{user_id}')
