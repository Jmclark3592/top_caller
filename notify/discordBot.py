# NOT USING AT THIS TIME - SEE TRACKER.PY I AM JUST USING WEBHOOK RIGHT NOW

import discord
import os
from dotenv import load_dotenv

# Load environment variables from .env file.
load_dotenv()


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
        await message.channel.send("@everyone Hello!")


client.run(os.getenv("DISCORD_TOKEN"))
