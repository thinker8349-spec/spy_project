from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/search")
def search():
    username = request.args.get("username", "").lower().strip()

    try:
        with open("database.json", "r") as f:
            db = json.load(f)
    except:
        return jsonify({"error": "DB not found"})

    for uid, user in db.get("users", {}).items():
        uname = str(user.get("username", "")).lower().strip()

        # 🔥 exact match (fast)
        if uname == username:
            return jsonify(user)

    return jsonify([])
