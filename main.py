import requests
import schedule
import time
import os
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def get_prices():
    try:
        url = "https://tgju.org"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        text = r.text
        
        # استخراج قیمت‌ها
        import re
        
        prices = {}
        
        # دلار
        match = re.search(r'price_dollar_rl["\']:["\']?(\d+)', text)
        prices['dollar'] = match.group(1) if match else "---"
        
        # طلا
        match = re.search(r'price_geram18["\']:["\']?(\d+)', text)
        prices['gold'] = match.group(1) if match else "---"
        
        # نفت
        match = re.search(r'price_oil["\']:["\']?(\d+)', text)
        prices['oil'] = match.group(1) if match else "---"
        
        # تتر
        match = re.search(r'price_tether["\']:["\']?(\d+)', text)
        prices['tether'] = match.group(1) if match else "---"
        
        # تون
        match = re.search(r'price_ton["\']:["\']?(\d+)', text)
        prices['ton'] = match.group(1) if match else "---"
        
        msg = "📊 قیمت لحظه‌ای\n\n"
        msg += f"💵 دلار: {prices['dollar']} ریال\n"
        msg += f"🥇 طلای ۱۸ عیار: {prices['gold']} ریال\n"
        msg += f"🛢 نفت: {prices['oil']} ریال\n"
        msg += f"💎 تتر: {prices['tether']} ریال\n"
        msg += f"📦 تون (گرام): {prices['ton']} ریال\n"
        
        return msg
    except Exception as e:
        return None

def send_message(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHANNEL_ID, "text": text})
    except:
        pass

def job():
    msg = get_prices()
    if msg:
        send_message(msg)

schedule.every(12).hours.do(job)

job()

while True:
    schedule.run_pending()
    time.sleep(60)
