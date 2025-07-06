from flask import Flask, request, jsonify, send_from_directory
import sqlite3, uuid, os, threading, time, requests

app = Flask(__name__)

DB_FILE = 'db.sqlite3'
SCREENSHOT_DIR = 'screenshots'
PLACEHOLDER_IMAGE = 'placeholder.png'

# Folder for screenshot
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                url TEXT,
                webhook_url TEXT,
                status TEXT,
                screenshot_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

@app.route('/screenshots', methods=['POST'])
def submit_screenshot():
    data = request.json
    url = data.get('url')
    webhook_url = data.get('webhook_url')

    if not url or not webhook_url:
        return jsonify({"error": "Missing url or webhook_url"}), 400

    job_id = str(uuid.uuid4())

    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            'INSERT INTO jobs (id, url, webhook_url, status) VALUES (?, ?, ?, ?)',
            (job_id, url, webhook_url, 'queued')
        )

    # Start background worker
    threading.Thread(target=process_job, args=(job_id, url, webhook_url)).start()

    return jsonify({"job_id": job_id, "status": "queued"})


def process_job(job_id, url, webhook_url):
    print(f"Processing job {job_id} for {url}")
    time.sleep(5) # delay 

    try:
        # copying placeholder
        screenshot_path = os.path.join(SCREENSHOT_DIR, f"{job_id}.png")
        with open(PLACEHOLDER_IMAGE, 'rb') as src, open(screenshot_path, 'wb') as dst:
            dst.write(src.read())

        with sqlite3.connect(DB_FILE) as conn:
            conn.execute(
                'UPDATE jobs SET status=?, screenshot_path=? WHERE id=?',
                ('completed', screenshot_path, job_id)
            )

        payload = {
            "job_id": job_id,
            "status": "completed",
            "screenshot_url": f"http://localhost:5000/screenshots/{job_id}"  #server
        }
        print(f"Calling webhook {webhook_url} with payload {payload}")
        requests.post(webhook_url, json=payload)

    except Exception as e:
        print(f"Error processing job {job_id}: {e}")
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute('UPDATE jobs SET status=? WHERE id=?', ('failed', job_id))

@app.route('/screenshots/<job_id>/status')
def get_status(job_id):
    with sqlite3.connect(DB_FILE) as conn:
        row = conn.execute('SELECT status FROM jobs WHERE id=?', (job_id,)).fetchone()
        if not row:
            return jsonify({"error": "Job not found"}), 404
        return jsonify({"job_id": job_id, "status": row[0]})

@app.route('/screenshots/<job_id>')
def get_screenshot(job_id):
    with sqlite3.connect(DB_FILE) as conn:
        row = conn.execute('SELECT status FROM jobs WHERE id=?', (job_id,)).fetchone()
        if not row:
            return jsonify({"error": "Job not found"}), 404

        status = row[0]
        if status != 'completed':
            return jsonify({"error": "Screenshot not ready"}), 400

    # image directory
    return send_from_directory(SCREENSHOT_DIR, f"{job_id}.png")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
