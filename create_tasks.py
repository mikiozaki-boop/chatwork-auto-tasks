import os
import requests

API_TOKEN = os.environ["CHATWORK_API_TOKEN"]
ROOM_ID = os.environ["CHATWORK_ROOM_ID"]

def get_members():
    url = "https://api.chatwork.com/v2/rooms/" + ROOM_ID + "/members"
    res = requests.get(
        url,
        headers={"X-ChatWorkToken": API_TOKEN}
    )
    members = res.json()
    for member in members:
        print(str(member["account_id"]) + " : " + member["name"])

get_members()
