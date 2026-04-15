from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # 🔥 VERY IMPORTANT (fixes Loveable issue)

# ✅ Home route
@app.route("/")
def home():
    return "API is running ✅"

# 🔍 Search route
@app.route("/search")
def search():
    username = request.args.get("username", "").lower().strip()

    if not username:
        return jsonify([])

    try:
        with open("database.json", "r") as f:
            db = json.load(f)
    except:
        return jsonify([])

    results = []

    for uid, user in db.get("users", {}).items():
        uname = str(user.get("username", "")).lower().strip()

        if username in uname:
            results.append(user)

    return jsonify(results)  # 🔥 ALWAYS LIST

# 🚀 Run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
