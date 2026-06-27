import requests
import schedule
import time
import os
import json

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def get_prices():
    try:
        url = "https://api.nobitex.ir/market/stats/?srcCurrency=btc&dstCurrency=rls"
        r = requests.get(url, timeout=10)
        data = r.json()
        
        # این API قیمت‌های دقیق تری داره
        msg = "📊 قیمت لحظه‌ای\n\n"
        msg += f"💵 دلار: {data.get('stats', {}).get('btc', {}).get('latest', 'N/A')} ریال\n"
        msg += "✅ به‌روز شد: الآن\n"
        
        return msg
    except:
        return None

def send_message(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHANNEL_ID, "text": text}, timeout=10)
        print("✅ پیام ارسال شد")
    except Exception as e:
        print(f"❌ خطا: {e}")

def job():
    msg = get_prices()
    if msg:
        send_message(msg)
    else:
        print("❌ قیمت‌ها دریافت نشد")

print("🤖 ربات شروع شد")
job()

schedule.every(12).hours.do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
