import os
import requests
from datetime import datetime

API_TOKEN = os.environ["CHATWORK_API_TOKEN"]
ROOM_ID   = os.environ["CHATWORK_ROOM_ID"]

TASKS = [
    {
        "name":      "田中",
        "accountId": "111111",
        "body":      "週次報告書の提出をお願いします",
        "timing":    "weekly",
        "weekday":   0,
        "day":       None,
    },
    {
        "name":      "佐藤",
        "accountId": "222222",
        "body":      "勤怠データの確認をお願いします",
        "timing":    "monthly",
        "weekday":   None,
        "day":       25,
    },
]

def create_task(task):
    url = f"https://api.chatwork.com/v2/rooms/{ROOM_ID}/tasks"
    res = requests.post(url,
        headers={"X-ChatWorkToken": API_TOKEN},
        data={"body": task["body"], "to_ids": task["accountId"], "limit_type": "none"}
