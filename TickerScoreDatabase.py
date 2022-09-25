from pymongo import MongoClient
import json
import PhoneTextSender as PTS


client = MongoClient(
    "mongodb+srv://saatvik:fuckmylife@cluster0.bak7hv2.mongodb.net/?retryWrites=true&w=majority"
)


db = client["phonenumbers"]
collection = db["ticker_scores"]


def count_DB():
    doc_count = collection.count_documents({})
    return doc_count


def add_to_DB(ticker, score, suggestion):
    if collection.find_one({"ticker": ticker}) == None:
        post = {"ticker": ticker, "score": score, "suggestion": suggestion}
        collection.insert_one(post)
    else:
        collection.find_one_and_update(
            {"ticker": ticker}, {"$set": {"score": score, "suggestion": suggestion}}
        )


def remove_from_DB(ticker):
    collection.find_one_and_delete({"ticker": ticker})
