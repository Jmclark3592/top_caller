# will track volume. When crypto volume and prices increase, it is often local or even cycle top

"""
Authenticate with the Yahoo API
Send requests to the Yahoo API to retrieve data
Process the data and check for the conditions you're interested in
When the conditions are met, send an HTTP POST request to your Discord webhook URL to send an alert
"""

import yfinance as yf

# import pandas as pd
# import numpy as np
from dotenv import load_dotenv
import os
import requests
import json
import datetime
import time

load_dotenv()
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

prev_volume = None

while True:
    today = datetime.date.today()
    df = yf.download("SOL-USD", start=today)

    if df.empty and prev_volume is not None and df.Volume.iloc[-1] > prev_volume * 1.01:
        print("Sending alert to discord")
        alert_content = (
            f"The volume has increased from {prev_volume} to {df.Volume.iloc[-1]}"
        )
        requests.post(
            DISCORD_WEBHOOK,
            data=json.dumps({"content": alert_content}),
            headers={"Content-Type": "application/json"},
        )
    if not df.empty:
        prev_volume = df.Volume.iloc[-1]  # in case the dataframe is empty

    time.sleep(86400)  # check daily for now

# print(df)
