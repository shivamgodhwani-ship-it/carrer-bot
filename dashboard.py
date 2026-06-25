from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import json
import os
from pathlib import Path
from datetime import datetime

app = Flask(__name__, static_folder="dashboard_ui")
CORS(app)

BASE = Path(__file__).parent

def load_json(path, default=[]):
    try:
        with open(BASE / path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default

def save_json(path, data):
    with open(BASE / path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


@app.get("/api/stats")
def stats():
    jobs = load_json("filtered_jobs.json")
    all_jobs = load_json("jobs.json")
    log = load_json("application_log.json")
    applied = [e for e in log if e.get("status") == "applied"]
    failed = [e for e in log if "failed" in str(e.get("status", "")) or "error" in str(e.get("status", ""))]
    return jsonify({
        "total_scraped": len(all_jobs),
        "qualified": len(set(j["link"] for j in jobs)),
        "applied": len(applied),
        "failed": len(failed),
        "pending": max(0, len(set(j["link"] for j in jobs)) - len(log)),
    })

@app.get("/api/jobs")
def get_jobs():
    jobs = load_json("filtered_jobs.json")
    log = load_json("application_log.json")
    log_map = {e["company"]: e for e in log}
    seen = set()
    result = []
    for job in jobs:
        key = job["link"]
        if key in seen:
            continue
        seen.add(key)
        log_entry = log_map.get(job["company"], {})
        job["status"] = log_entry.get("status", "pending")
        job["applied_at"] = log_entry.get("time", "")
        screenshots_dir = BASE / "screenshots"
        screenshot = ""
        if screenshots_dir.exists():
            safe = job["company"].replace(" ", "_").replace("/", "_")
            matches = list(screenshots_dir.glob(f"*{safe}*"))
            if matches:
                screenshot = "screenshots/" + matches[-1].name
        job["screenshot"] = screenshot
        result.append(job)
    result.sort(key=lambda x: x.get("score", 0), reverse=True)
    return jsonify(result)

@app.get("/api/log")
def get_log():
    return jsonify(load_json("application_log.json"))

@app.post("/api/job/update_status")
def update_status():
    data = request.json
    log = load_json("application_log.json")
    for entry in log:
        if entry["company"] == data["company"]:
            entry["status"] = data["status"]
            entry["notes"] = data.get("notes", "")
            save_json("application_log.json", log)
            return jsonify({"ok": True})
    log.append({
        "company": data["company"],
        "job": data.get("job", ""),
        "status": data["status"],
        "notes": data.get("notes", ""),
        "time": datetime.now().strftime("%H:%M:%S")
    })
    save_json("application_log.json", log)
    return jsonify({"ok": True})

@app.get("/screenshots/<path:filename>")
def serve_screenshot(filename):
    return send_from_directory(BASE / "screenshots", filename)

@app.get("/")
def index():
    return send_from_directory(BASE / "dashboard_ui", "index.html")

if __name__ == "__main__":
    os.makedirs(BASE / "dashboard_ui", exist_ok=True)
    os.makedirs(BASE / "screenshots", exist_ok=True)
    print("\n🚀 Dashboard running at http://localhost:5000\n")
    app.run(debug=False, port=5000)
