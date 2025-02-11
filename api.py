#!/usr/bin/env python
# -*- coding: utf-8 -*-
import platform
from quart import Quart, request, jsonify
from quart_cors import cors
from store.xhs import xhs_store_sql
from cache import iredis
from tools import utils

app = Quart(__name__)
app = cors(app)


@app.route('/content/<string:platform>', methods=['GET'])
async def get_content(platform):
    try:
        rows = await xhs_store_sql.query_content()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/update/cookie', methods=['POST'])
async def update_cookie():
    data = await request.json
    try:
        print(f"update_cookie data: {data}")
        user_id = data.get("user_id")
        cookie = data.get("cookie")
        platform = data.get("platform")
        # 检查是否提供了必要的参数
        if not user_id or not cookie or not platform:
            return jsonify({"error": "缺少必要的参数"}), 400

        # 将cookie写入Redis
        iredis.update_cookie(platform, user_id, cookie)
    except Exception as e:
        return jsonify({"error": f"更新cookie出错: {str(e)}"}), 500
    return jsonify({"message": "更新cookie成功"}), 200


@app.route('/crawl/creator/data', methods=['POST'])
async def crawl_creator_data():
    data = await request.json
    try:
        # 从请求数据中提取任务信息
        print(f"update_cookie data: {data}")
        platform = data.get("platform")
        creator_id = data.get("creator_id")
        user_id = data.get("user_id")
        count = data.get("count")
        # 检查是否提供了必要的参数
        if not platform or not creator_id or not user_id:
            return jsonify({"error": "缺少必要的参数"}), 400
        
        task = {
            "platform": platform,
            "creator_id": creator_id,
            "user_id": user_id,
            "count": count
        }
        # 将任务信息写入Redis
        iredis.push_crawler_task("creator", task)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify({'status': 'success'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
