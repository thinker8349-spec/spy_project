import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://www.imvu.com/"
}

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
            "following": info.get("approx_following_count"),
        }
    except:
        return None
