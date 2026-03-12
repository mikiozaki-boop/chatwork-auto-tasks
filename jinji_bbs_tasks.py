import os
import requests
import jpholiday
from datetime import datetime, timedelta

API_TOKEN = os.environ["CHATWORK_API_TOKEN"]
ROOM_ID = os.environ["CHATWORK_ROOM_ID"]

MEMBERS = [
    {"name": "安田璃奈子", "accountId": "4374516"},
    {"name": "島仲弘英",   "accountId": "8390505"},
]

TASK_BODY = "【連絡】休暇報告書提出の期限のお知らせ\n今月の休暇報告書を期限までに提出してください。提出先はグループチャット「人事BBS」にお願いします。\n（休暇報告書格納先：https://www.chatwork.com/#!rid359970432-2033482443050455040）"

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

def create_task(member, limit_timestamp):
    url = "https://api.chatwork.com/v2/rooms/" + ROOM_ID + "/tasks"
    res = requests.post(
        url,
        headers={"X-ChatWorkToken": API_TOKEN},
        data={
            "body": TASK_BODY,
            "to_ids": member["accountId"],
            "limit_type": "date",
            "limit": limit_timestamp
        }
    )
    if res.status_code == 200:
        print(member["name"] + ": OK")
    else:
        print(member["name"] + ": NG " + res.text)

def main():
    now = datetime.now()
    if now.day != 15:
        print("今日は15日ではないため実行しません")
        return

    limit_day = get_limit_date(now.year, now.month)
    limit_timestamp = int(datetime(limit_day.year, limit_day.month, limit_day.day, 23, 59, 59).timestamp())

    for member in MEMBERS:
        create_task(member, limit_timestamp)

if __name__ == "__main__":
    main()
