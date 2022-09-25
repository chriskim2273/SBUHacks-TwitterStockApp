import json
import math
from numpy import number
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from threading import *

model_name = "ProsusAI/finbert"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)


def label_to_value(connotation, number_of_tweets):
    score = -math.log(connotation["score"] ** 2, 10)
    score = 1 / math.e ** connotation["score"]
    score = connotation["score"] ** 2
    if connotation["label"] == "negative":
        return -1 * score  # / number_of_tweets  # * score...
    elif connotation["label"] == "positive":
        return 1 * score  # / number_of_tweets
    else:
        return 0


def label_to_value_raw(connotation, number_of_tweets):
    score = connotation["score"]  # ** 2
    if connotation["label"] == "negative":
        return -1 * score  # * score...
    elif connotation["label"] == "positive":
        return 1 * score
    else:
        return 0


scores = {}
raw_scores = {}
ticker_count = {}


class sentiment_tracker:
    def __init__(self):
        self.scores = {}
        self.raw_scores = {}
        self.ticker_count = {}

    def __getScores__(self, key):
        return self.scores[key]

    def __setScores__(self, key, value):
        self.scores[key] = value

    def __addScores__(self, key, add):
        self.scores[key] += add

    def __getRawScores__(self, key):
        return self.raw_scores[key]

    def __setRawScores__(self, key, value):
        self.raw_scores[key] = value

    def __addRawScores__(self, key, add):
        self.raw_scores[key] += add

    def __getTickerCount__(self, key):
        return self.ticker_count[key]

    def __getAllTickerCount__(self):
        return self.ticker_count

    def __setTickerCount__(self, key, value):
        self.ticker_count[key] = value

    def __incrementTickerCount__(self, key):
        self.ticker_count[key] += 1
        print(self.ticker_count[key])

    def __getAllScores__(self):
        return self.scores

    def __getAllRawScores__(self):
        return self.raw_scores


class sentiment_analyzer(Thread):
    def __init__(self, tweets, number_of_tweets, sentiment_tracker):
        super(sentiment_analyzer, self).__init__()
        self.tweets = tweets
        self.number_of_tweets = number_of_tweets
        self.sentiment_tracker = sentiment_tracker
        self.test = {}

    def calculateScores(self):
        self.test["JOE"] = "JOE"

        json = self.tweets
        number_of_tweets = self.number_of_tweets

        results = []
        for tweet in json["tweets"]:
            result = {
                "connotation": classifier(tweet["text"]),
                "id": tweet["id"],
                "ticker": json["ticker"],
            }
            if "$" + result["ticker"].lower() in tweet["text"].lower():
                if result["ticker"] in self.sentiment_tracker.__getAllTickerCount__():
                    self.sentiment_tracker.__incrementTickerCount__(result["ticker"])
                else:
                    self.sentiment_tracker.__setTickerCount__(result["ticker"], 0)
                results.append(result)
                print("Text: " + tweet["text"] + "\n" + "Result: " + str(result))
                print(
                    "Tracker: "
                    + str(self.sentiment_tracker.__getTickerCount__(result["ticker"]))
                )

        for result in results:
            ticker = result["ticker"]
            score = label_to_value(result["connotation"][0], number_of_tweets)
            raw_score = label_to_value_raw(result["connotation"][0], number_of_tweets)
            # print(score)
            if ticker not in self.sentiment_tracker.__getAllScores__():
                self.sentiment_tracker.__setScores__(ticker, score)
            else:
                self.sentiment_tracker.__addScores__(ticker, score)
            if ticker not in self.sentiment_tracker.__getAllRawScores__():
                self.sentiment_tracker.__setRawScores__(ticker, raw_score)
            else:
                self.sentiment_tracker.__addRawScores__(ticker, raw_score)

    def run(self):
        self.calculateScores()
