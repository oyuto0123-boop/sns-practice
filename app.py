from flask import Flask, render_template, request

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
    category = request.args.get("category")
    conn = get_connection()
    with conn.cursor() as cur:
        if category:
            cur.execute(
                    "SELECT id, body, category, prefecture, created_at FROM posts WHERE category = %s ORDER BY created_at DESC LIMIT 20",
                    (category,)
                    )
        else:
            cur.execute(
                    "SELECT id, body, category, prefecture, created_at FROM posts ORDER BY created_at DESC LIMIT 20"
                    )
        posts = cur.fetchall()
    conn.close()
    return render_template("index.html", posts=posts)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
