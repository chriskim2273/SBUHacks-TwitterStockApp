from flask import Flask, request, url_for, redirect, render_template
import yfinance

# import PhoneNumDataBase as PB
import TickerDataBase as TB
import requests

from ticker_suggestor import ticker_suggestor

app = Flask(__name__)


def getTickerData():
    tickers = TB.getAllTickers()
    tickerData = [[], [], []]
    for ticker in tickers:
        if ticker["suggestion"] == "NEUTRAL":
            tickerData[1].append(ticker["ticker"])
        elif ticker["suggestion"] == "NO":
            tickerData[0].append(ticker["ticker"])
        else:
            tickerData[2].append(ticker["ticker"])
    return tickerData


@app.get("/")
def index():
    tickerData = getTickerData()
    return render_template("index.html", tickerData=tickerData)


@app.post("/search")
def search_tinker():
    tinkerSearch = request.form.get("searchedTick")
    url = (
        "https://financialmodelingprep.com/api/v3/search-ticker?query="
        + tinkerSearch
        + "P&limit=10&exchange=NASDAQ&apikey=c3067dd09e4d92d4be0a9a2da2f6b88d"
    )
    result = requests.get(url=url)
    searchData = result.json()
    tickerData = getTickerData()
    return render_template("search.html", tickerData=tickerData, searchData=searchData)


@app.post("/enter")
def apply_on_ticker():
    ticker = str(request.form.get("enteredTick")).upper()
    yf_ticker = yfinance.Ticker(ticker)
    print(yf_ticker.info)
    appTicker = {
        "decision": None,
        "name": None,
        "numTweets": None,
    }
    if yf_ticker.info["regularMarketPrice"] == None:
        print("NOT VALID")
        tickerData = getTickerData()
        return render_template("index.html", tickerData=tickerData, appTicker=appTicker)
    suggestor = ticker_suggestor([ticker], 50)
    result = suggestor.getSuggestion()
    if result["NEUTRAL"] == []:
        if result["NO"] == []:
            appTicker["decision"] = "YES"
            appTicker["name"] = result["YES"][0]
        else:
            appTicker["decision"] = "NO"
            appTicker["name"] = result["NO"][0]
    else:
        appTicker["decision"] = "NEUTRAL"
        appTicker["name"] = result["NEUTRAL"][0]
    tickerData = getTickerData()
    return render_template("index.html", tickerData=tickerData, appTicker=appTicker)


# @app.route('/subscribe', methods = ['GET', 'POST'])
# def subscribe_func():
#     if request.method == 'POST':
#         userNum = request.form.get('phoneNum')
#         userTicker = request.form.get('ticker')
#         if userNum.isdigit() and len(userNum) == 10:
#             PB.add_to_DB(userNum, userTicker)
#             return render_template("subscribe.html")
#         else:
#             return "Incorrect input try again."
#     else:
#         return render_template('index.html', tinkerData=None)

# @app.route('/update', methods = ['GET', 'POST'])
# def update():
#     if request.method == 'POST':
#         userNum = request.form.get('phoneNum')
#         userTicker = request.form.get('ticker')
#         if len(userNum) == 10:
#             PB.update_from_DB(userNum, userTicker)
#             return render_template('index.html', tinkerData=None)
#         else:
#             return "Incorrect input, try again"
#     else:
#         return render_template('index.html', tinkerData=None)

# @app.route('/unsubscribe', methods = ['GET', 'POST'])
# def unsubscribe_func():
#     if request.method == 'POST':
#         userNum = request.form.get('phoneNum')
#         if userNum.isdigit() and len(userNum) == 10:
#             PB.remove_from_DB(userNum)
#             return render_template("unsubscribe.html")
#         else:
#             return "Incorrect input try again."
#     else:
#         return render_template('index.html', tinkerData=None)

#   <link rel= "stylesheet" type= "text/css" href= "{{ url_for('static',filename='styles/mainpage.css') }}">
#   DO NOT change anything in the form sections in the index.html section, unless you want to deal with it.
#   MongoDB credentials saatvik : fuckmylife
