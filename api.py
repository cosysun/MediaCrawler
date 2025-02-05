#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_cors import CORS

from store import xhs_store_sql
from var import crawlers_var

app = Flask(__name__)
CORS(app)


@app.route('/content/<string:platform>', methods=['GET'])
def get_content(platform):
    # 在这里实现获取特定平台内容的逻辑
    # 例如，您可以调用相应的函数来获取数据
    rows = xhs_store_sql.query_content(platform)
    return jsonify(rows), 200


@app.route('/crawl/data/<string:platform>', methods=['POST'])
async def crawl_data(platform):
    # 在这里实现获取特定平台和关键字内容的逻辑
    # 例如，您可以调用相应的函数来获取数据
    crawler = crawlers_var.get(platform)
    if not crawler:
        return jsonify({'error': 'Crawler not found'}), 404
    await crawler.get_creators_and_notes()
    pass


def start():
    app.run(host='0.0.0.0', port=5001, debug=False)
