from flask import Flask, jsonify, request
import datetime
import json
import requests
import sqlite3

app = Flask(__name__)

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
    conn.close()
    return jsonify(subject_list)


if __name__ == "__main__":
    app.run(debug=False, use_reloader=True, host='152.66.177.17')
