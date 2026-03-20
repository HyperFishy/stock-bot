

import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://quack.food/purchase"
OUT_OF_STOCK_TEXT = "out of stock - check back soon"

ALERT_WEBHOOK = "https://discord.com/api/webhooks/1484438605773668374/VO_fd4JzkXtI0OUubDoXIQG8hmYIKgyHOMolMyuz6KL5dDLU5AV29uQsKrSUV3JWbH98"
STATUS_WEBHOOK = "https://discord.com/api/webhooks/1484438696366313614/qtqJmdCC2_dp81V8ItxfdiGHVFYUJ_hcm4gXzI0_Ea3HUZZU8oQEBNw2PZhVnTFBBWuw"

headers = {
    "User-Agent": "Mozilla/5.0"
}


def send(webhook, message):
    if "PASTE" in webhook:
        print("Webhook not set")
        return

    response = requests.post(
        webhook,
        json={"content": message},
        timeout=10
    )
    response.raise_for_status()


def main():
    response = requests.get(URL, headers=headers, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(" ", strip=True).lower()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if OUT_OF_STOCK_TEXT in text:
        status = "OUT OF STOCK"
    else:
        status = "IN STOCK / CHANGED"
        send(ALERT_WEBHOOK, f"🚨 STOCK ALERT\n{URL}")

    send(STATUS_WEBHOOK, f"[{now}] STATUS: {status}")
    print(f"[{now}] STATUS: {status}")


if __name__ == "__main__":
    main()
