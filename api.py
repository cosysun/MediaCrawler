#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_cors import CORS
from crawlers import CrawlerManager
from store.xhs import xhs_store_sql

app = Flask(__name__)
CORS(app)


@app.route('/content/<string:platform>', methods=['GET'])
async def get_content(platform):
    try:
        rows = await xhs_store_sql.query_content()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/crawl/data/<string:platform>', methods=['POST'])
async def crawl_data(platform):
    crawler = CrawlerManager.get_crawler(platform)
    if not crawler:
        return jsonify({'error': 'Crawler not found'}), 404
    try:
        await crawler.get_creators_and_notes()
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def start():
    app.run(host='0.0.0.0', port=5001, debug=True)
