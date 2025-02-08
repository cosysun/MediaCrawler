import threading
import schedule
import time
from cache import iredis
from tools import utils


def process_crawler_task():
    try:
        task = iredis.pop_crawler_task()
        if not task:
            utils.logger.info("No task to process.")
            return
        # todo
    except Exception as e:
        utils.logger.error(f"process_crawler_task 发生错误, err: {str(e)}")


def start():
    schedule.every(10).seconds.do(process_crawler_task)

    def run_schedule():
        while True:
            schedule.run_pending()
            time.sleep(1)

    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.start()
