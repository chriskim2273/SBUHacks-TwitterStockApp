from pymongo import MongoClient
from bson.json_util import dumps
import json

client = MongoClient("mongodb+srv://saatvik:fuckmylife@cluster0.bak7hv2.mongodb.net/?retryWrites=true&w=majority")
db = client['phonenumbers']
collection = db['ticker_scores']

def getAllTickers():
    tickers = json.loads(dumps(collection.find()))
    print(tickers)
    return tickers
