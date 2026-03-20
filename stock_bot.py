import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://quack.food/purchase"
CHECK_EVERY_SECONDS = 10
OUT_OF_STOCK_TEXT = "out of stock - check back soon"

headers = {
    "User-Agent": "Mozilla/5.0"
}

print("Starting test... (Press Control + C to stop)\n")

while True:
    try:
        response = requests.get(URL, headers=headers, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(" ", strip=True).lower()

        if OUT_OF_STOCK_TEXT in text:
            status = "OUT OF STOCK"
        else:
            status = "IN STOCK / CHANGED"

        print(f"[{datetime.now().strftime('%H:%M:%S')}] STATUS: {status}")

    except Exception as e:
        print("Error:", e)

    time.sleep(CHECK_EVERY_SECONDS)
