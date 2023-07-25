# will track volume. When crypto volume and prices increase, it is often local or even cycle top

# see Serious Python, try to output volume into postgreSQL

import yfinance as yf

# import pandas as pd
# import numpy as np
import sqlite3
from dotenv import load_dotenv
import os
import requests
import json
import datetime
import time

load_dotenv()
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
conn = sqlite3.connect(
    "/Users/justinclark/Workspace/top_caller/volume_tracker/volume_sqlite.db"
)

cursor = conn.cursor()
cursor.execute(
    """
            CREATE TABLE IF NOT EXISTS volume_data (
                Date TEXT PRIMARY KEY,
                Open_Val REAL,
                High REAL,
                Low REAL,
                Close REAL,
                Adj_Close REAL,
                Volume BIGINT
            )
        """
)
conn.commit()

prev_volume = None

prev_day = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()

cursor.execute(
    """
               SELECT Volume FROM volume_data WHERE Date = ?
               """,
    (prev_day,),
)
row = cursor.fetchone()
prev_volume = row[0] if row is not None else None

while True:
    today = datetime.date.today()
    df = yf.download("SOL-USD", start=today)

    if (
        not df.empty
        and prev_volume is not None
        and df.Volume.iloc[-1] > prev_volume * 1.01
    ):
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
        date_str = today.isoformat()
        open_val = df["Open"].iloc[-1]
        high = df["High"].iloc[-1]
        low = df["Low"].iloc[-1]
        close = df["Close"].iloc[-1]
        adj_close = df["Adj Close"].iloc[-1]
        volume = df["Volume"].iloc[-1]

        cursor.execute(
            """
            INSERT OR REPLACE INTO volume_data VALUES (?,?,?,?,?,?,?)""",
            (date_str, open_val, high, low, close, adj_close, volume),
        )
        prev_volume = volume
        conn.commit()

    time.sleep(86400)

conn.close()

# today = datetime.date.today()
# df = yf.download("SOL-USD", start="2023-07-16")
# print(df)
