from flask import Flask

import os
import pymysql

app = Flask(__name__)

def get_connection():
    return pymysql.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            database=os.environ['DB_NAME'],
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
    )

@app.route("/")
def index():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT id, body, category, prefecture, created_at FROM posts ORDER BY created_at DESC")
        posts = cur.fetchall()
    conn.close()
    return str(posts)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
