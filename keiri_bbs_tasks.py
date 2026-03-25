import os
import requests
import jpholiday
from datetime import datetime, timedelta

API_TOKEN = os.environ["CHATWORK_API_TOKEN"]
KEIRI_ROOM_ID = "404376004"

MEMBERS = [
    {"name": "安田璃奈子", "accountId": "4374516"},
    {"name": "島仲弘英",   "accountId": "8390505"},
]

TASK_BODY = "[info][title]【連絡】立替精算書提出のお願い[/title]提出期限までに立替精算書を作成し領収書を添付し部長→社長へ提出をお願いします。立替経費精算書#共通.xlsx[/info]"

def get_delivery_date(year, month):
    d = datetime(year, month, 25)
    while d.weekday() >= 5 or jpholiday.is_holiday(d):
        d -= timedelta(days=1)
    return d

def get_nth_business_day(year, month, n):
    count = 0
    d = datetime(year, month, 1)
    last_day = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
    while d < last_day:
        if d.weekday() < 5 and not jpholiday.is_holiday(d.date()):
            count += 1
            if count == n:
                return d
        d += timedelta(days=1)

def get_next_month(year, month):
    if month == 12:
        return year + 1, 1
    return year, month + 1

def create_task(member, limit_timestamp):
    url = "https://api.chatwork.com/v2/rooms/" + KEIRI_ROOM_ID + "/tasks"
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
    delivery_date = get_delivery_date(now.year, now.month)
    if now.date() != delivery_date.date():
        print("今日は配信日ではないため実行しません")
        return

    next_year, next_month = get_next_month(now.year, now.month)
    limit_day = get_nth_business_day(next_year, next_month, 3)
    limit_timestamp = int(datetime(limit_day.year, limit_day.month, limit_day.day, 14, 59, 59).timestamp())
    print("期限日: " + str(limit_day.date()))

    for member in MEMBERS:
        create_task(member, limit_timestamp)

if __name__ == "__main__":
    main()
