import discord
import os
from dotenv import load_dotenv

# Load environment variables from .env file.
load_dotenv())


# create an instance of client
client = discord.Client()


# register an event
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")


"""
def get_quote():
    response = requests.get('https://api.etherscan.io/api', params=params)
#creating my own for whale tracker
@client.event
async def whale_alert(prev_bal, current_bal):
    if prev_bal is not None and prev_bal - current_bal >= 10000:
"""
client.run(os.getenv("DISCORD_TOKEN"))
