from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "API is running ✅"

@app.route("/search")
def search():
    username = request.args.get("username", "").lower().strip()

    if not username:
        return jsonify([])

    try:
        with open("database.json", "r") as f:
            db = json.load(f)
    except Exception as e:
        return jsonify({"error": str(e)})

    # 🔥 FAST SEARCH (stops early)
    for uid, user in db.get("users", {}).items():
        uname = str(user.get("username", "")).lower().strip()

        if username in uname:
            return jsonify(user)  # return first match instantly

    return jsonify([])

# 🔥 VERY IMPORTANT
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
