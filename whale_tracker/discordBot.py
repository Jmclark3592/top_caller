import discord
import os
import requests


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


client.run("MTEyOTA0Njk1NTg5MzQ2OTIyNg.GbmXhk.qJLIixsuX8QCEQDv1-hYVx51TWyoYwWeQZAz6I")
