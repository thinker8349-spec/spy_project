from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/search")
def search():
    username = request.args.get("username")

    with open("database.json") as f:
        db = json.load(f)

    results = []

    for uid, user in db["users"].items():
        if username.lower() in str(user.get("username", "")).lower():
            results.append(user)

    return jsonify(results)

app.run(host="0.0.0.0", port=5000)
