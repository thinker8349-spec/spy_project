import requests
import json
import time
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://www.imvu.com/"
}

DB_FILE = "database.json"

# ✅ Create DB if not exists
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({"users": {}}, f)

# 📦 Load DB
def load_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

# 💾 Save DB
def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)

# 👤 Get profile
def get_profile(user_id):
    try:
        url = f"https://api.imvu.com/profile/profile-user-{user_id}"
        res = requests.get(url, headers=HEADERS)

        data = res.json()
        denorm = data.get("denormalized", {})
        info = denorm.get(url, {}).get("data", {})

        if not info:
            return None

        return {
            "username": info.get("avatar_name"),
            "bio": info.get("tagline"),
            "gender": info.get("gender"),
            "country": info.get("country"),
            "profile_image": info.get("image"),
            "followers": info.get("approx_follower_count"),
        }
    except:
        return None

# 👥 Extract users + live image
def extract_users(chat_link):
    try:
        res = requests.get(chat_link + "/participants", headers=HEADERS)
        data = res.json()

        denorm = data.get("denormalized", {})
        key = chat_link + "/participants"

        items = denorm.get(key, {}).get("data", {}).get("items", [])

        users = []

        for u in items:
            uid = u.split("-")[-1]
            user_data = denorm.get(u, {}).get("data", {})

            users.append({
                "user_id": uid,
                "image": user_data.get("look_image")
            })

        return users
    except:
        return []

# 🚀 MAIN SCRAPER
def run():
    db = load_db()
    counter = 0

    while True:
        print("\n🔥 FULL SCAN STARTED")

        url = "https://api.imvu.com/room_list/room_list-389766535-explore/rooms?limit=20"

        while url:
            res = requests.get(url, headers=HEADERS)
            data = res.json()

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
                    user_id = user["user_id"]
                    image = user["image"]

                    # 🆕 create user
                    if user_id not in db["users"]:
                        db["users"][user_id] = {
                            "images": [],
                            "rooms": []
                        }

                    # 👤 PROFILE
                    profile = get_profile(user_id)
                    if profile:
                        db["users"][user_id].update(profile)

                    # 👕 OUTFIT IMAGES
                    if image:
                        if image not in db["users"][user_id]["images"]:
                            db["users"][user_id]["images"].append(image)

                    # 🔥 ROOM HISTORY (NEW FEATURE)
                    if room_name not in db["users"][user_id]["rooms"]:
                        db["users"][user_id]["rooms"].append(room_name)

                    # 🔥 LAST SEEN
                    db["users"][user_id]["last_seen"] = room_name

                    counter += 1

                    # 💾 FAST SAVE
                    if counter % 10 == 0:
                        save_db(db)
                        print("💾 Auto-saved")

                    time.sleep(0.4)

                # 💾 Save after each room
                save_db(db)
                print("💾 Saved after room")

            url = data.get("next")

        print("\n🔁 Restarting scan...\n")
        time.sleep(5)


if __name__ == "__main__":
    run()
