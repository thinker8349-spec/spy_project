import requests
import json
import time
from datetime import datetime

DATABASE = "database.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

# 🔥 LOAD DATABASE
def load_db():
    try:
        with open(DATABASE, "r") as f:
            return json.load(f)
    except:
        return {"users": {}}


# 🔥 SAVE DATABASE
def save_db(db):
    with open(DATABASE, "w") as f:
        json.dump(db, f, indent=2)


# 🔥 GET ROOMS (IMVU API)
def get_rooms():
    url = "https://api.imvu.com/room"
    try:
        r = requests.get(url, headers=HEADERS)
        data = r.json()
        return data.get("denormalized", {})
    except:
        return {}


# 🔥 GET ROOM DETAILS
def get_room_detail(room_id):
    url = f"https://api.imvu.com/chat/room-{room_id}"
    try:
        r = requests.get(url, headers=HEADERS)
        return r.json()
    except:
        return {}


# 🔥 PROCESS ROOMS
def scan():
    db = load_db()
    rooms = get_rooms()

    print("🔥 FULL SCAN STARTED")

    for key, room in rooms.items():

        try:
            room_id = room.get("room_id")
            room_name = room.get("name")

            if not room_id or not room_name:
                continue

            detail = get_room_detail(room_id)

            participants = []

            for item in detail.get("denormalized", {}).values():
                if item.get("type") == "user":

                    user_id = item.get("id")
                    username = item.get("username")
                    avatar = item.get("thumbnail_url")

                    if not user_id or not username:
                        continue

                    participants.append({
                        "user_id": user_id,
                        "username": username,
                        "avatar": avatar
                    })

            # ROOM IMAGE
            room_image = room.get("image_url")

            timestamp = int(time.time())

            # 🔥 SAVE FOR EACH USER
            for user in participants:

                uid = str(user["user_id"])

                if uid not in db["users"]:
                    db["users"][uid] = {
                        "username": user["username"],
                        "profile_image": user["avatar"],
                        "sessions": []
                    }

                session = {
                    "room_name": room_name,
                    "room_image": room_image,
                    "users": participants,
                    "timestamp": timestamp
                }

                db["users"][uid]["sessions"].append(session)

                # LIMIT DATA (keep last 100 sessions)
                db["users"][uid]["sessions"] = db["users"][uid]["sessions"][-100:]

                print(f"Saved: {user['username']} in {room_name}")

        except Exception as e:
            print("Error:", e)

    save_db(db)
    print("✅ Scan complete")


# 🔁 LOOP
while True:
    scan()
    print("🔁 Restarting scan...\n")
    time.sleep(60)  # every 1 min
