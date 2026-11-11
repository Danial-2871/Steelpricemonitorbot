
import os
import json
import urllib.request
import urllib.parse

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

BASE = f"https://api.telegram.org/bot{TOKEN}/"

def telegram(method, data=None):
    encoded = urllib.parse.urlencode(data or {}).encode()
    request = urllib.request.Request(BASE + method, data=encoded)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode())

# دریافت پیام‌های جدید
result = telegram("getUpdates", {"limit": 100})
updates = result.get("result", [])

if not updates:
    print("پیام جدیدی دریافت نشد.")

else:
    for item in updates:
        msg = item.get("message", {})
        text = msg.get("text", "")

        if text and str(msg.get("chat", {}).get("id")) == CHAT_ID:
            reply = (
                "پیام شما دریافت شد.\n\n"
                "متن پیام:\n" + text[:3000]
            )

            telegram("sendMessage", {
                "chat_id": CHAT_ID,
                "text": reply
            })

    # تأیید دریافت پیام‌ها برای جلوگیری از تکرار
    last_id = max(item["update_id"] for item in updates)
    telegram("getUpdates", {"offset": last_id + 1, "limit": 1})

print("بررسی پیام‌ها پایان یافت.")
