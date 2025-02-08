# -*- coding: utf-8 -*-
# @Desc    : mediacrawler db 管理
import asyncio
from typing import Dict, Optional

import aiofiles
import aiomysql

import config
from store.async_db import AsyncMysqlDB
from tools import utils


class DBPool:
    _instance: Optional[AsyncMysqlDB] = None
    _pool = None
    
    @classmethod
    async def get_pool(cls):
        if not cls._pool:
            cls._pool = await aiomysql.create_pool(
                host=config.RELATION_DB_HOST,
                port=config.RELATION_DB_PORT,
                user=config.RELATION_DB_USER,
                password=config.RELATION_DB_PWD,
                db=config.RELATION_DB_NAME,
                autocommit=True
            )
        return cls._pool

    @classmethod
    async def get_db(cls) -> AsyncMysqlDB:
        if not cls._instance:
            pool = await cls.get_pool()
            cls._instance = AsyncMysqlDB(pool)
        return cls._instance

    @classmethod
    async def close(cls):
        if cls._pool:
            cls._pool.close()
            await cls._pool.wait_closed()
            cls._pool = None
            cls._instance = None


async def init_db():
    """初始化数据库连接"""
    await DBPool.get_db()
    utils.logger.info("[init_db] init database connection successful")


async def init_table_schema():
    """
    用来初始化数据库表结构，请在第一次需要创建表结构的时候使用，多次执行该函数会将已有的表以及数据全部删除
    Returns:

    """
    utils.logger.info("[init_table_schema] begin init mysql table schema ...")
    async_db_obj: AsyncMysqlDB = await DBPool.get_db()
    async with aiofiles.open("schema/tables.sql", mode="r", encoding="utf-8") as f:
        schema_sql = await f.read()
        await async_db_obj.execute(schema_sql)
        utils.logger.info("[init_table_schema] mediacrawler table schema init successful")
        await DBPool.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(init_table_schema())
