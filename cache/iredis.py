import pickle
from typing import Any
import redis
from config import db_config


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


def pop_crawler_task() -> Any:
    task = RedisPool().getConn().lpop('crawler_task')
    if task:
        return pickle.loads(task)
    return None


def push_crawler_task(task: Any) -> None:
    serialized_task = pickle.dumps(task)
    RedisPool().getConn().rpush('crawler_task', serialized_task)
    