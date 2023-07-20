# Tweeting an alert / notification
# DO I NEED ENDPOINT URL FROM AWS EC2? Using https://localhost in the app settings

import os
from dotenv import load_dotenv
import numpy as np
import tweepy

load_dotenv()

consumer_key = os.getenv("TWITTER_API_KEY")
consumer_secret_key = os.getenv("TWITTER_SECRET_KEY")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


tweet = input("enter the tweet: ")
# Generate text tweet
api.update_status(tweet)

# tweet_text = input("enter the tweet ")

# Generate text tweet with media (image)
"""image_path = input("enter the path of the image ")

status = api.update_with_media(image_path, tweet_text)
api.update_status(tweet_media)"""