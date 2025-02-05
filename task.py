import threading
from reply import process_inquiry_replies
import schedule
import time
import json
from lib.ali1688 import ali1688
from lib import alibaba
import requests
import os
import serviceConfig
import logger
import mysql
from lib.func_txy import calculate_md5_hash
from PIL import Image
import myProxy
import iredis
import common


def process_send_task():
    try:
        task = iredis.pop_send_task(serviceConfig.args.userid)
        if not task:
            return
        task_data = json.loads(task)
        pid = task_data.get('pid')
        offer_id = task_data.get('offer_id')
        user_id = task_data.get('user_id')
        message = task_data.get('message')
        sku = task_data.get('sku')
        result = mysql.get_product_info_by_userid(pid, offer_id, sku, user_id)
        if result is None:
            logger.error(
                f"pid: {pid}, sku: {sku}, offer_id: {offer_id}, 未找到商品信息")
            return
        login_id = result[4]

        ret = common.send_message_to_aliwangwang(
            pid, offer_id, sku, user_id, login_id, [message], str(int(time.time())))
        if not ret:
            logger.error(
                f"pid: {pid}, sku: {sku}, offer_id: {offer_id}, 消息发送失败")
            return

        if not mysql.update_inquiry_status(pid, sku, offer_id, mysql.INQUIRY_STATUS_INQUIRED):
            logger.error(
                f"pid: {pid}, sku: {sku}, offer_id: {offer_id}, 更新询价状态失败")
    except Exception as e:
        logger.error(f"process_send_task 发生错误, err: {str(e)}")


def run_schedule_task(task_function):
    while True:
        task_function()
        time.sleep(1)


schedule.every(10).seconds.do(process_send_task)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


schedule_thread = threading.Thread(target=run_schedule)
schedule_thread.start()
