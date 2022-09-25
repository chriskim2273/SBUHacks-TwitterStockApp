from lib2to3.pgen2.token import NUMBER
import math
import timeit
from class_twitter_fetch import getTweets, tweet_jsons_tracker
import class_twitter_fetch
import analyze_sentiment
from analyze_sentiment import sentiment_analyzer, sentiment_tracker
import TickerScoreDatabase

trending_tickers = [
    "META",
    "GME",
    "RBLX",
    "MSFT",
]
NUMBER_OF_TWEETS = 500

start = timeit.default_timer()


class ticker_suggestor:
    def __init__(self, tickers, number_of_tweets):
        self.tickers = tickers
        self.number_of_tweets = number_of_tweets

    def getSuggestion(self):
        tickers = self.tickers
        number_of_tweets = self.number_of_tweets
        threads = []

        tweet_jsons = class_twitter_fetch.tweet_jsons_tracker()

        for ticker in tickers:
            fetcher = getTweets(ticker, number_of_tweets, tweet_jsons)
            threads.append(fetcher)
            fetcher.start()

        for thread in threads:
            thread.join()

        threads = []
        # print(twitter_fetch.tweet_jsons)

        score_tracker = analyze_sentiment.sentiment_tracker()

        for tweet in tweet_jsons.tweet_jsons:
            analyzer = sentiment_analyzer(tweet, number_of_tweets, score_tracker)
            threads.append(analyzer)
            analyzer.start()
            # calculateScores(tweets, number_of_tweets)

        for thread in threads:
            # print(str(thread))
            print(thread.test["JOE"])
            thread.join()

        for score in score_tracker.__getAllScores__():
            print(
                "ticker: "
                + str(score)
                + " ("
                + str(score_tracker.__getTickerCount__(score))
                + ") "
            )
            score_tracker.__setScores__(
                score,
                score_tracker.__getScores__(score)
                / (score_tracker.__getTickerCount__(score)),
            )

        print(score_tracker.__getAllScores__())
        # print(score_tracker.__getRawScores__())

        SUGGESTIONS = {"YES": [], "NO": [], "NEUTRAL": []}

        counter = 0
        for score in score_tracker.__getAllScores__():
            counter += 1
            suggest = ""
            if abs(score_tracker.__getScores__(score)) > 0.1:
                if score_tracker.__getScores__(score) < 0:
                    SUGGESTIONS["NO"].append(score)
                    suggest = "NO"
                elif score_tracker.__getScores__(score) > 0:
                    SUGGESTIONS["YES"].append(score)
                    suggest = "YES"
            else:
                SUGGESTIONS["NEUTRAL"].append(score)
                suggest = "NEUTRAL"

            TickerScoreDatabase.add_to_DB(
                score, score_tracker.__getScores__(score), suggest
            )
            SUGGESTIONS["NUMBER_OF_TWEETS"] = score_tracker.__getTickerCount__(score)
            SUGGESTIONS["SCORE"] = score_tracker.__getScores__(score)
        if counter != 1:
            del SUGGESTIONS["NUMBER_OF_TWEETS"]
            del SUGGESTIONS["SCORE"]

        return SUGGESTIONS

    # print(getSuggestion(trending_tickers, NUMBER_OF_TWEETS))

    end = timeit.default_timer()

    print(str(end - start))
