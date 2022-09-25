# -*- coding: utf-8 -*-
from io import StringIO
import tweepy
from datetime import date
import yfinance as yf
import demoji
from threading import *

# auth = tweepy.OAuth1UserHandler(
#   consumer_key = 'UsdF3pJdZirVrDAFyq8UhCI24', consumer_secret = 'Iqi0oiDEqeZF3ro3LBdFMrBD75DKDajCmmtYEsb9RxH4zQOg7M'#, access_token, access_token_secret
# )
auth = tweepy.OAuth2BearerHandler(
    "AAAAAAAAAAAAAAAAAAAAAKSvhQEAAAAAZvFe76BXfNl3Ln4sbLJMavC5Mcw%3DQEKUSqvrrKsK8QMjS5BXjyteBv03Y7qyeQf2Ri4YvDagihfhuW"
)

api = tweepy.API(auth)

# print(api.available_trends())
# api = tweepy.API(auth)
client = tweepy.Client(
    consumer_key="3PLSvoemDuzyF6WYgXt0ZH0Mm",
    consumer_secret="eY6439bv30Qce9GG9kg3FUinIIXD9BMdClZTe4nH8BHeyqZ4mv",
    access_token="1573499265543979019-GQGPsr8uIDvIPvVG0sPxuPR5JVL03X",
    access_token_secret="6FfmKf76t2F5epc2aSRDM1JFUSIUjgSKLYJXEnXuRx3E0",
    bearer_token="AAAAAAAAAAAAAAAAAAAAAKSvhQEAAAAAZvFe76BXfNl3Ln4sbLJMavC5Mcw%3DQEKUSqvrrKsK8QMjS5BXjyteBv03Y7qyeQf2Ri4YvDagihfhuW",
)

response_template = {"tweets": [], "ticker": "", "date_updated": ""}
tweet_template = {"text": "", "id": ""}

# Maybe also consider the companies and also account for it in the calculation.


def isEnglish(s):
    try:
        s.encode(encoding="utf-8").decode("ascii")
    except UnicodeDecodeError:
        return False
    else:
        return True


def removeStringDiscrepancies(sentence):
    if "-" in sentence:
        sentence = sentence.replace("-", " down ")
    if "+" in sentence:
        sentence = sentence.replace("+", " up ")
    if '"' in sentence:
        sentence = sentence.replace('"', "")
    if "'" in sentence:
        sentence = sentence.replace("'", "")
    return sentence


def getTweetTexts(ticker, tweet_count):
    yf_ticker = yf.Ticker(ticker)
    company_name = yf_ticker.info["longName"]

    print(ticker)

    # Last 7 days of tweets
    tweets = api.search_tweets(
        q="$" + ticker,
        result_type="mixed",
        count=tweet_count,
        tweet_mode="extended",
    )

    # Add both restults and use a set to remove intersectional tweets.

    response = response_template.copy()

    response["date_updated"] = str(date.today())
    response["ticker"] = ticker
    response["company"] = company_name

    if len(tweets) > 0:
        for tweet in tweets:
            # string = StringIO(tweet.full_text)
            tweet_body = tweet_template.copy()

            lines = tweet.full_text.split("\n")
            new_text = ""
            for line in lines:
                for sentence in line.split(". "):

                    # replace emojis with text to allow machine learning model to work properly
                    emojis_found = demoji.findall(sentence)
                    for emoji in emojis_found:
                        sentence = sentence.replace(emoji, emojis_found[emoji])

                    # Check if its english, if not, skip
                    # if not isEnglish(sentence):
                    #    continue

                    # Try to isolate the text about the ticker and avoid text about other tickers.
                    # Also avoids links
                    if ("$" + ticker).lower() in sentence.lower():  # or (
                        # ("$" in sentence) and ("https://" not in sentence)

                        # Make it so that the model can handle + and - values.
                        # Clean up string

                        sentence = removeStringDiscrepancies(sentence)

                        new_text += sentence
                        new_text += " "
            ###

            tweet_body["text"] = new_text
            # tweet_body["text"] = tweet.full_text
            tweet_body["id"] = tweet.id
            response["tweets"].append(tweet_body)
            # print(response)
    else:
        response["tweets"] = "N/A"
    return response
