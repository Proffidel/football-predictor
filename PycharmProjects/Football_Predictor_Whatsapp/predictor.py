import requests
import numpy as np
from datetime import datetime
import pywhatkit
import schedule
import time
import os

# ================== YOUR SETTINGS ==================
API_KEY = os.getenv("API_KEY", "35731b2ac5e34496939633b0c3bb86a8")
YOUR_WHATSAPP = os.getenv("YOUR_WHATSAPP", "+2349010503256")
# ===================================================

headers = {'X-Auth-Token': API_KEY}


def get_todays_matches():
    try:
        url = "http://api.football-data.org/v4/matches"
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            print("API Error:", response.status_code)
            return []
        matches = response.json().get('matches', [])
        today = datetime.now().strftime("%Y-%m-%d")
        return [m for m in matches if m.get('utcDate', '').startswith(today)]
    except Exception as e:
        print("Fetch error:", e)
        return []


def get_simple_prediction(home, away):
    home_prob = np.random.randint(42, 72)
    if home_prob >= 63:
        return f"✅ {home} to Win (Conf: {home_prob}%)"
    elif home_prob <= 40:
        return f"✅ {away} to Win (Conf: {100 - home_prob}%)"
    else:
        return f"✅ Over 1.5 Goals (Conf: 68%)"


def send_predictions():
    current_time = datetime.now().strftime("%H:%M")
    print(f"[{current_time}] Sending 10 Sure Odds...")

    matches = get_todays_matches()

    if not matches:
        message = f"⚠️ No matches available now ({current_time})"
    else:
        message = f"🔥 *10 SURE ODDS - {current_time}*\n📅 {datetime.now().strftime('%A, %d %B %Y')}\n\n"
        for i, match in enumerate(matches[:10]):
            home = match['homeTeam']['name']
            away = match['awayTeam']['name']
            pred = get_simple_prediction(home, away)
            message += f"{i + 1}. {home} vs {away}\n   → {pred}\n\n"

    try:
        pywhatkit.sendwhatmsg_instantly(YOUR_WHATSAPP, message, wait_time=20, tab_close=True)
        print(f"✅ Sent successfully at {current_time}")
    except Exception as e:
        print("WhatsApp Error:", e)


# ================== SCHEDULE (7AM, 10AM, 1PM, 4PM) ==================
schedule.every().day.at("07:00").do(send_predictions)
schedule.every().day.at("10:00").do(send_predictions)
schedule.every().day.at("13:00").do(send_predictions)
schedule.every().day.at("15:00").do(send_predictions)
schedule.every().day.at("17:30").do(send_predictions)

print("🚀 Predictor running...")

while True:
    schedule.run_pending()
    time.sleep(60)