import json
import time
import os
from core.profile import get_profile
from core.users import extract_users
from core.rooms import get_rooms

DB_FILE = "database.json"

# create db if not exists
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({"users": {}}, f)

def load_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)

def run():
    db = load_db()
    counter = 0

    while True:
        print("🔥 FULL SCAN STARTED")

        url = "https://api.imvu.com/room_list/room_list-389766535-explore/rooms?limit=20"

        while url:
            data = get_rooms(url)
            rooms = data.get("denormalized", {})

            for key, value in rooms.items():

                if "data" not in value or "name" not in value["data"]:
                    continue

                room_name = value["data"]["name"]
                chat = value.get("relations", {}).get("chat")

                print("🏠 Room:", room_name)

                if not chat:
                    continue

                users = extract_users(chat)

                for user in users:
                    uid = user["user_id"]
                    img = user["image"]

                    if uid not in db["users"]:
                        db["users"][uid] = {"images": []}

                    # 🔥 always fetch profile
                    profile = get_profile(uid)
                    if profile:
                        db["users"][uid].update(profile)

                    if img and img not in db["users"][uid]["images"]:
                        db["users"][uid]["images"].append(img)

                    db["users"][uid]["last_seen"] = room_name

                    counter += 1

                    if counter % 10 == 0:
                        save_db(db)
                        print("💾 Auto-saved")

                    time.sleep(0.4)

            url = data.get("next")

        print("🔁 Restarting scan...\n")
        time.sleep(5)

if __name__ == "__main__":
    run()
