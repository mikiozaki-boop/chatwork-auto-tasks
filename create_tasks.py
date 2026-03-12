import os
import requests
from datetime import datetime

API_TOKEN = os.environ["CHATWORK_API_TOKEN"]
ROOM_ID = os.environ["CHATWORK_ROOM_ID"]

TASKS = [
    {
        "name": "安田璃奈子",
        "accountId": "4374516",
        "body": "【連絡】休暇報告書提出の期限のお知らせ\n今月の休暇報告書を期限までに提出してください。提出先はグループチャット「人事BBS」にお願いします。\n（休暇報告書格納先：https://www.chatwork.com/#!rid359970432-2033482443050455040）",
        "timing": "monthly",
        "day": 12,
    },
    {
        "name": "島仲弘英",
        "accountId": "8390505",
        "body": "【連絡】休暇報告書提出の期限のお知らせ\n今月の休暇報告書を期限までに提出してください。提出先はグループチャット「人事BBS」にお願いします。\n（休暇報告書格納先：https://www.chatwork.com/#!rid359970432-2033482443050455040）",
        "timing": "monthly",
        "day": 12,
    },
    {
        "name": "尾崎美希",
        "accountId": "2769500",
        "body": "【連絡】休暇報告書提出の期限のお知らせ\n今月の休暇報告書を期限までに提出してください。提出先はグループチャット「人事BBS」にお願いします。\n（休暇報告書格納先：https://www.chatwork.com/#!rid359970432-2033482443050455040）",
        "timing": "monthly",
        "day": 12,
    },
]

def create_task(task):
    now = datetime.now()
    limit_date = datetime(now.year, now.month, 23, 23, 59, 59)
    limit_timestamp = int(limit_date.timestamp())

    url = "https://api.chatwork.com/v2/rooms/" + ROOM_ID + "/tasks"
    res = requests.post(
        url,
        headers={"X-ChatWorkToken": API_TOKEN},
        data={
            "body": task["body"],
            "to_ids": task["accountId"],
            "limit_type": "date",
            "limit": limit_timestamp
        }
    )
    if res.status_code == 200:
        print(task["name"] + ": OK")
    else:
        print(task["name"] + ": NG " + res.text)

def main():
    now = datetime.now()
    for task in TASKS:
        if task["timing"] == "monthly" and task["day"] == now.day:
            create_task(task)

if __name__ == "__main__":
    main()
