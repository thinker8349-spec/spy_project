import json

def search_user(username):
    with open("database.json") as f:
        db = json.load(f)

    username = username.lower()

    results = []

    for uid, user in db["users"].items():
        if username in str(user.get("username", "")).lower():
            results.append((uid, user))

    return results
