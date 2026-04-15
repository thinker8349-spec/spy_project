import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

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
