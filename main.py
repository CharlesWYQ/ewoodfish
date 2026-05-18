# -*- coding: utf-8 -*-
# @Time : 2026/5/18 08:23
# @Author : CharlesWYQ
# @Email : charleswyq@foxmail.com
# @File : main.py
# @Project : ewoodfish
# @Details : 


# app.py（完整版）
from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__, static_folder='static')
db_path = 'data/fish_click.db'


def init_db():
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS stats
                     (
                         id
                         INTEGER
                         PRIMARY
                         KEY,
                         total_clicks
                         INTEGER
                         DEFAULT
                         0
                     )''')
        c.execute('INSERT INTO stats (total_clicks) VALUES (0)')
        conn.commit()
        conn.close()


@app.before_request
def before_request():
    init_db()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


# API 路由（不变）
@app.route('/api/count', methods=['GET'])
def get_count():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT total_clicks FROM stats WHERE id = 1')
    count = c.fetchone()[0]
    conn.close()
    return jsonify({'total_clicks': count})


@app.route('/api/click', methods=['POST'])
def add_click():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('UPDATE stats SET total_clicks = total_clicks + 1 WHERE id = 1')
    conn.commit()
    c.execute('SELECT total_clicks FROM stats WHERE id = 1')
    count = c.fetchone()[0]
    conn.close()
    return jsonify({'total_clicks': count})


# 👇 新增：兜底路由，处理所有静态资源
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
