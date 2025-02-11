import asyncio
import schedule
import time
from base import base_crawler
from cache import iredis
from tools import utils
from crawlers import CrawlerManager

async def process_crawler_task():
    try:
        while True:
            task = iredis.pop_crawler_task("creator")
            if not task:
                utils.logger.info("No task to process.")
                return

            crawler = await CrawlerManager.get_crawler(task["platform"])
            if crawler:
                await crawler.crawl(base_crawler.CREATOR, [task["creator_id"]])
            else:
                utils.logger.error(f"Invalid crawler for platform: {task['platform']}")
                return
            time.sleep(1)
        
    except Exception as e:
        utils.logger.error(f"process_crawler_task 发生错误, err: {str(e)}")


async def run_schedule():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


if __name__ == "__main__":
    schedule.every(10).seconds.do(lambda: asyncio.create_task(process_crawler_task()))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_schedule())
