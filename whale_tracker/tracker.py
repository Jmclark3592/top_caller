# API allows 5 calls per second
# whale address to track: 0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe
# my address: 0x15378FA7495bac16040877F7E17c6547481687F6

import requests

# import json
# import smtplib
# from email.message import EmailMessage
import time
import os


# connect to API
url = "https://api.etherscan.io/api"
address = "0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe"
API_KEY = os.getenv("API_KEY")


params = {
    "module": "account",
    "action": "balance",
    "address": address,
    "tag": "latest",
    "apikey": API_KEY,
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

    if prev_bal is not None and prev_bal - current_bal >= 10000:
        print("Sending alert - will replace with actual alert")
        # configure to send a text or email

    prev_bal = current_bal

    time.sleep(5)  # polling API every 60s
