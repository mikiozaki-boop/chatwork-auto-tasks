import os
import requests
from datetime import datetime

API_TOKEN = os.environ["CHATWORK_API_TOKEN"]
ROOM_ID = os.environ["CHATWORK_ROOM_ID"]

TASKS = [
    {
        "name": "尾崎 美希",
        "accountId": "mikiozaki",
        "body": "[info][title]【連絡】休暇報告書提出の期限のお知らせ[/title]今月の休暇報告書提出の期限は3/24とします。提出先はグループチャット「人事BBS」にお願いします。
（休暇報告書格納先：
https://www.chatwork.com/#!rid359970432-2033482443050455040[/info]",
        "timing": "weekly",
        "weekday": 0,
        "day": None,
    },
   
]

def create_task(task):
    url = "https://api.chatwork.com/v2/rooms/" + ROOM_ID + "/tasks"
    res = requests.post(
        url,
        headers={"X-ChatWorkToken": API_TOKEN},
        data={
            "body": task["body"],
            "to_ids": task["accountId"],
            "limit_type": "none"
        }
    )
    if res.status_code == 200:
        print(task["name"] + ": OK")
    else:
        print(task["name"] + ": NG " + res.text)

def main():
    now = datetime.now()
    for task in TASKS:
        if task["timing"] == "daily":
            create_task(task)
        elif task["timing"] == "weekly" and task["weekday"] == now.weekday():
            create_task(task)
        elif task["timing"] == "monthly" and task["day"] == now.day:
            create_task(task)

if __name__ == "__main__":
    main()
