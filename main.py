import requests
import schedule
import time
from datetime import datetime

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_ID = "@Pricee_Iran_bot"

def get_prices():
    try:
        url = "https://tgju.org"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        
        # قیمت‌ها رو استخراج کن
        import re
        
        dollar = re.search(r'price-dollar.*?(\d+)', r.text)
        gold = re.search(r'geram18.*?(\d+)', r.text)
        oil = re.search(r'oil.*?(\d+)', r.text)
        tether = re.search(r'tether.*?(\d+)', r.text)
        ton = re.search(r'ton.*?(\d+)', r.text)
        
        msg = "📊 قیمت لحظه‌ای\n\n"
        msg += "💵 دلار: " + (dollar.group(1) if dollar else "---") + " ریال\n"
        msg += "🥇 طلای ۱۸ عیار: " + (gold.group(1) if gold else "---") + " ریال\n"
        msg += "🛢 نفت: " + (oil.group(1) if oil else "---") + " ریال\n"
        msg += "💎 تتر: " + (tether.group(1) if tether else "---") + " ریال\n"
        msg += "📦 تون (گرام): " + (ton.group(1) if ton else "---") + " ریال\n"
        
        return msg
    except:
        return None

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHANNEL_ID, "text": text})

def job():
    msg = get_prices()
    if msg:
        send_message(msg)
        print("✅ پیام ارسال شد!")

# هر 12 ساعت یکبار اجرا شو
schedule.every(12).hours.do(job)

print("ربات شروع به کار کرد!")
job()

while True:
    schedule.run_pending()
    time.sleep(60)
