import os
import time
import requests

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

SYMBOL = "PAXGUSDT"
STEP = 100


def get_price():
    url = "https://api.binance.com/api/v3/ticker/price"
    response = requests.get(
        url,
        params={"symbol": SYMBOL},
        timeout=10
    )
    response.raise_for_status()
    return float(response.json()["price"])


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=10
    )

    response.raise_for_status()


price = get_price()

send_telegram(
    f"🤖 بدأ بوت PAXG\n\n"
    f"السعر الحالي: ${price:,.2f}\n"
    f"التنبيه كل ±${STEP}"
)

last_alert_price = price

while True:
    try:
        price = get_price()

        difference = price - last_alert_price

        if difference >= STEP:
            send_telegram(
                f"🟢 PAXG ارتفاع\n\n"
                f"السعر السابق: ${last_alert_price:,.2f}\n"
                f"السعر الحالي: ${price:,.2f}\n"
                f"الارتفاع: +${difference:,.2f}"
            )

            last_alert_price = price

        elif difference <= -STEP:
            send_telegram(
                f"🔴 PAXG هبوط\n\n"
                f"السعر السابق: ${last_alert_price:,.2f}\n"
                f"السعر الحالي: ${price:,.2f}\n"
                f"الهبوط: -${abs(difference):,.2f}"
            )

            last_alert_price = price

        time.sleep(20)

    except Exception as e:
        print("Error:", e)
        time.sleep(20)
