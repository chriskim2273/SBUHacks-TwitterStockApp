from ast import literal_eval
from flask import Flask, request, url_for, redirect, render_template
import PhoneNumDataBase as PB
import ticker_suggestor

app = Flask(__name__)


@app.route("/")
def hello_world():
    print("sdasda")
    return render_template("index.html")


@app.route("/get_suggestions", methods=["GET"])
def get_suggestions():
    trending_tickers = [
        "META",
        "GME",
        "RBLX",
        "MSFT",
        "SGML",
        "TRMD",
        "STNG",
        "ASC",
        "TNK",
        "PRPH",
        "SRTS",
        "INSW",
        "DCPH",
        "SBR",
        "FREY",
        "MCK",
    ]
    tickers = request.args.get("tickers")
    tickers = literal_eval(tickers)
    suggestor = ticker_suggestor.ticker_suggestor()
    return suggestor.getSuggestion(tickers, 50)


@app.route("/get_single_suggestion", methods=["GET"])
def get_single_suggestion():
    ticker = str(request.args.get("ticker"))
    tickers = [ticker]
    suggestor = ticker_suggestor.ticker_suggestor(tickers, 50)
    return suggestor.getSuggestion()


@app.route("/subscribe", methods=["GET", "POST"])
def subscribe_func():
    if request.method == "POST":
        userNum = request.form.get("sub")
        if userNum.isdigit() and len(userNum) == 10:
            PB.add_to_DB(PB.count_DB() + 1, userNum)
            return render_template("subscribe.html")
        else:
            return "Incorrect input try again."

    else:
        return render_template(url_for(hello_world))


@app.route("/unsubscribe", methods=["GET", "POST"])
def unsubscribe_func():
    if request.method == "POST":
        userNum = request.form.get("unsub")
        if userNum.isdigit() and len(userNum) == 10:
            PB.remove_from_DB(userNum)
            return render_template("unsubscribe.html")
        else:
            return "Incorrect input try again."
    else:
        return render_template(url_for(hello_world))


#   <link rel= "stylesheet" type= "text/css" href= "{{ url_for('static',filename='styles/mainpage.css') }}">
#   DO NOT change anything in the form sections in the index.html section, unless you want to deal with it.
# MongoDB credentials saatvik : fuckmylife
