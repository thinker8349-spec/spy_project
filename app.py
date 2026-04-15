from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# ✅ Home route (for testing)
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

        # 🔥 partial + case-insensitive search
        if username in uname:
            results.append(user)

    return jsonify(results)  # ✅ ALWAYS return list

# 🚀 Run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
