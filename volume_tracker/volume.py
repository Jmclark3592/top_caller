# Will track volume. When crypto volume and prices increase, it is often local or even cycle top

# see Serious Python, try to output volume into postgreSQL

# NOTe that I had to clone this under a diff directory in EC2, top_caller_database:
# git clone -b database https://github.com/Jmclark3592/top_caller.git top_caller_database

# I am outputting to SQLite which is not outputting volume so i added a aws s3 bucket to try that.


import yfinance as yf
import sqlite3
import csv
import boto3
from dotenv import load_dotenv
import os
import requests
import json
import datetime
import time

load_dotenv()
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
conn = sqlite3.connect(
    "volume_sqlite.db"
)  # Connects to database in the current directory

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
                Volume INTEGER 
            )
        """
)
conn.commit()


prev_day = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()

cursor.execute(
    """
               SELECT Volume FROM volume_data WHERE Date = ?
               """,
    (prev_day,),
)
row = cursor.fetchone()

s3 = boto3.client("s3")
bucket = "volume"  # bucket name i gave it when creating with AWS
csv_file = "volume_data.csv"

prev_volume = None
print("Row content:", row)
prev_volume = float(row[0]) if row is not None else None


while True:
    today = datetime.date.today()
    df = yf.download("SOL-USD", start=today)

    if (
        not df.empty
        and prev_volume is not None
        and df.Volume.iloc[-1] > (prev_volume + 5000)
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
        volume = int(df["Volume"].iloc[-1])
        print(type(volume), volume)

        cursor.execute(
            """
            INSERT OR REPLACE INTO volume_data VALUES (?,?,?,?,?,?,?)""",
            (date_str, open_val, high, low, close, adj_close, volume),
        )
        prev_volume = volume
        conn.commit()

    cursor.execute("SELECT * FROM volume_data")
    rows = cursor.fetchall()

    with open("volume_data.csv", "w", newline="") as csvfile:  # write to csv file
        writer = csv.writer(csvfile)
        writer.writerow(
            ["Date", "Open_Val", "High", "Low", "Close", "Adj_Close", "Volume"]
        )
        writer.writerows(rows)
    s3.upload_file("volume_data.csv", "volume", "volume_data.csv")
    time.sleep(86400)  # daily

conn.close()
