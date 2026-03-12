import os
import requests
import jpholiday
from datetime import datetime, timedelta

API_TOKEN = os.environ["CHATWORK_API_TOKEN"]
ROOM_ID = os.environ["CHATWORK_ROOM_ID"]

TASKS = [
    {
        "name": "安田璃奈子",
        "accountId": "4374516",
        "body": "【連絡】休暇報告書提出のお願い\n今月の休暇報告書を期限までに提出してください。提出先はグループチャット「人事BBS」にお願いします。\n（休暇報告書格納先：https://www.chatwork.com/#!rid359970432-2033482443050455040）",
        "timing": "monthly",
        "day": 15,
    },
    {
        "name": "島仲弘英",
        "accountId": "8390505",
        "body": "【連絡】休暇報告書提出のお願い\n今月の休暇報告書を期限までに提出してください。提出先はグループチャット「人事BBS」にお願いします。\n（休暇報告書格納先：https://www.chatwork.com/#!rid359970432-2033482443050455040）",
        "timing": "monthly",
        "day": 15,
    },
    {
        "name": "尾崎美希",
        "accountId": "2769500",
        "body": "【連絡】休暇報告書提出のお願い\n今月の休暇報告書を期限までに提出してください。提出先はグループチャット「人事BBS」にお願いします。\n（休暇報告書格納先：https://www.chatwork.com/#!rid359970432-2033482443050455040）",
        "timing": "monthly",
        "day": 15,
    },
]

def get_limit_date(year, month):
    base = datetime(year, month, 20)
    count = 0
    d = base + timedelta(days=1)
    while count < 2:
        if d.weekday() < 5 and not jpholiday.is_holiday(d):
            count += 1
            if count == 2:
                return d
        d += timedelta(days=1)

def create_task(task, limit_timestamp):
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
    limit_day = get_limit_date(now.year, now.month)
    limit_timestamp = int(datetime(limit_day.year, limit_day.month, limit_day.day, 23, 59, 59).timestamp())

    for task in TASKS:
        if task["timing"] == "monthly" and task["day"] == now.day:
            create_task(task, limit_timestamp)

if __name__ == "__main__":
    main()
