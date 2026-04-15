import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_rooms(url):
    res = requests.get(url, headers=HEADERS)
    return res.json()
