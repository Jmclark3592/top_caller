# API allows 5 calls per second
# whale address to track: 0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe
# my address: 0x15378FA7495bac16040877F7E17c6547481687F6

import requests
import json
from dotenv import load_dotenv

# import smtplib?
# from email.message import EmailMessage?
import time
import os

# connect to API
url = "https://api.etherscan.io/api"
address = "0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe"
load_dotenv()
ETHERSCAN_TOKEN = os.getenv("ETHERSCAN_TOKEN")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

params = {
    "module": "account",
    "action": "balance",
    "address": address,
    "tag": "latest",
    "apikey": ETHERSCAN_TOKEN,
}

prev_bal = None

while True:
    response = requests.get(url, params=params)
    data = response.json()
    assert (
        "result" in data
    ), 'API response has changed: no "result" field.'  # assert that 'result' still in api dictionary
    current_bal = float(data["result"]) / 10**18
    print(f"Current Balance: {current_bal} ETH")

    if prev_bal is not None and prev_bal - current_bal >= 4900:
        print("Sending alert to discord")
        alert_content = f"The balance has decreased by over 4900 ETH! New balance: {current_bal} ETH"
        requests.post(
            DISCORD_WEBHOOK,
            data=json.dumps({"content": alert_content}),
            headers={"Content-Type": "application/json"},
        )

    prev_bal = current_bal

    time.sleep(3600)  # pulling API every hour (set to 5s during testing)
