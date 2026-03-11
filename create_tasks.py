import os
import requests
from datetime import datetime

API_TOKEN = os.environ["CHATWORK_API_TOKEN"]
ROOM_ID   = os.environ["CHATWORK_ROOM_ID"]

TASKS = [
    {
        "name":      "田中",        # 担当者名（メモ用）
        "accountId": "111111",      # ChatworkのアカウントID
        "body":      "週次報告書の提出をお願いします",
        "timing":    "weekly",      # 毎週
        "weekday":   0,             # 0=月曜
        "day":       None,
    },
    {
        "name":      "佐藤",
        "accountId": "222222",
        "body":      "勤怠データの確認をお願いします",
        "timing":    "monthly",     # 毎月
        "weekday":   None,
        "day":       25,            # 毎月25日
    },
]

def create_task(task):
    url = f"https://api.chatwork.com/v2/rooms/{ROOM_ID}/tasks"
    res = requests.post(url,
        headers={"X-ChatWorkToken": API_TOKEN},
        data={"body": task["body"], "to_ids": task["accountId"], "limit_type": "none"}
    )
    print(f"[{task['name']}] {'✅ 成功' if res.status_code == 200 else '❌ 失敗: ' + res.text}")

def main():
    now = datetime.now()
    for task in TASKS:
        should_run = (
            task["timing"] == "daily" or
            (task["timing"] == "weekly"  and task["weekday"] == now.weekday()) or
            (task["timing"] == "monthly" and task["day"]     == now.day)
        )
        if should_run:
            create_task(task)

if __name__ == "__main__":
    main()
```

**④ 右上の「Commit changes」ボタンをクリック→「Commit changes」で保存**

---

### 📄 ファイル2：`create_tasks.yml`（自動実行の設定）

**① 再び「Add file」→「Create new file」をクリック**

**② ファイル名に以下を入力（スラッシュを入力するとフォルダが自動で作られます）**
```
.github/workflows/create_tasks.yml
