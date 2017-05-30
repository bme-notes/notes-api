from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import datetime
import json
import requests
import sqlite3

def list_to_dict(list):
    return {'name': list[0], 'updated': list[1], 'url': list[2]}

app = Flask(__name__)
CORS(app)

@app.route('/')
def default():
    return '<a href="https://bme-notes.github.io">https://bme-notes.github.io</a>'


@app.route('/update/', methods=['POST'])
def update_note():
    data = request.get_json(force=True)

    if 'release' not in data or 'repository' not in data:
        return 'Invalid request!'

    if len(data['release']['assets']) == 0:
        return 'No release!'

    name = data['repository']['name']
    updated = data['release']['published_at']
    url = data['release']['assets'][0]['browser_download_url']

    db_file = "database.sqlite"
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    cur.execute("SELECT name FROM subjects WHERE name = ?", (name,))
    if cur.rowcount == 1:
        cur.execute("UPDATE subjects SET updated = datetime(?), url = ?", (updated, url,))
    else:
        cur.execute("INSERT INTO subjects VALUES(?, ?, ?)", (name, updated, url,))
    conn.commit()
    conn.commit()
    return 'Successful update!'


@app.route('/update-times/', methods=['GET'])
def list_notes():
    db_file = "database.sqlite"
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT name, datetime(updated) AS updated, url FROM subjects")
    subject_list = cur.fetchall()
    result_list = []
    for entry in subject_list:
        result_list.append(list_to_dict(entry))
    conn.close()
    return jsonify(result_list)


if __name__ == "__main__":
    app.run(debug=False, use_reloader=True, host='0.0.0.0')
