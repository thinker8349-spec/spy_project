import requests
import json
import time
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://www.imvu.com/",
    "cookie": "_gid=GA1.2.2027050784.1776155689; _gcl_au=1.1.1825522660.1776155690; _ga_7281G7S0PH=GS2.2.s1776155691$o1$g0$t1776155691$j60$l0$h0; __qca=P1-bc5e9804-597e-4589-ae74-1b1531752dfd; WZRK_G=61fa6433aad5455ea23c282943a35d23; sncd=1%2C1776155795%2CeNoztrA0NzMzNTYFAAmNAeU%3D%2CP7UzFgliHN; _imvu_avnm=36ehs; login_username=hsdhjsg@gmail.com; LoggedInWithAlloy=true; osCsid=cf0091aa5ca7e06184bf688474406ebe; prefer_alloy=1; _pin_unauth=dWlkPVlUUXdOR001WTJNdFpUbGlaUzAwTVRNMkxUazRORGN0TW1WbVpXTXdNbVptT0RaaQ; _fbp=fb.1.1776155791565.717017433958807740; fpestid=MSrgYVEsy4NiKEpD-PSNZgkJ699LuOExAdPkVgqusLZVzS3UACb5X_KPMoq018J9fKjNdg; _cc_id=554dff4e68acf49f5f1f9c284b20fe02; panoramaId_expiry=1776242204810; panoramaId=704bc485a7721b6fb1588b769cdfa9fb927aa8f0ac5611b281a70538eab410f6; panoramaIdType=panoDevice; __utma=1.2058603683.1776155689.1776155793.1776155793.1; __utmz=1.1776155793.1.1.utmcsr=imvu.com|utmccn=(referral)|utmcmd=referral|utmcct=/next/home/; imvufp=1735521669; acx=dhttx|^MSsqyQ==|LKB09gCa3gg=|$ipatx|^MSsqyQ==|4KB09gCa3gg=|$pt|^H4sIAJ383WkA/6uuBQBDv6ajAgAAAA==; idx=dxx|^23b46048-057c-4b61-a9d4-3ea9d540a551|$mx|^e1bc123e-05d9-4c36-88d0-b2ffd852098d; appier_utmz=%7B%7D; _atrk_siteuid=rMWKdRqvpGHEk1Tk; alloy_landing_cookie=1; _gat=1; _atrk_ssid=bOyVkEqjJToZIgFSi_XC0j; appier_page_isView_PageView_ATM=856abb48bc67ebc6d128702a59c6502bc2df8309df5d92c282ebf532f24e6962; appier_pv_counterViewTwoPages_ATM=0; appier_page_isView_ViewTwoPages_ATM=856abb48bc67ebc6d128702a59c6502bc2df8309df5d92c282ebf532f24e6962; window_session=window_btzqqdbjUxfF/4MLnaG49w==; appier_pv_counterPageView_ATM=1; _ga_LN6M4L5CGR=GS2.1.s1776200899$o3$g1$t1776200931$j28$l0$h0; _ga=GA1.2.2058603683.1776155689; _ga_H9JKW05XRK=GS2.2.s1776200902$o3$g1$t1776200932$j30$l0$h0; _atrk_sessidx=6; WZRK_S_R97-5W9-9K7Z=%7B%22p%22%3A2%2C%22s%22%3A1776200920%2C%22t%22%3A1776200935%7D"
}
DB_FILE = "database.json"

# ✅ Create DB if not exists
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({"users": {}}, f)

def load_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

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

# 👥 Extract users
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

        # ✅ UPDATED ROOM API (WORKING BASE)
        url = "https://api.imvu.com/room_list/room_list-389766535-explore/rooms?limit=20"

        while url:
            try:
                res = requests.get(url, headers=HEADERS)
                data = res.json()
            except:
                print("❌ Failed to fetch rooms")
                break

            denorm = data.get("denormalized", {})

            if not denorm:
                print("⚠️ No room data (check cookie or endpoint)")
                break

            for key, value in denorm.items():

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

                    # 🆕 Create user
                    if user_id not in db["users"]:
                        db["users"][user_id] = {
                            "images": [],
                            "rooms": []
                        }

                    # 👤 Profile
                    profile = get_profile(user_id)
                    if profile:
                        db["users"][user_id].update(profile)

                    # 👕 Outfit images
                    if image:
                        if image not in db["users"][user_id]["images"]:
                            db["users"][user_id]["images"].append(image)

                    # 🔥 Room history
                    if room_name not in db["users"][user_id]["rooms"]:
                        db["users"][user_id]["rooms"].append(room_name)

                    # 🔥 Last seen
                    db["users"][user_id]["last_seen"] = room_name

                    counter += 1

                    # 💾 Auto save
                    if counter % 10 == 0:
                        save_db(db)
                        print("💾 Auto-saved")

                    time.sleep(0.3)

                # 💾 Save after each room
                save_db(db)

            url = data.get("next")

        print("🔁 Restarting scan...\n")
        time.sleep(5)


if __name__ == "__main__":
    run()
