from pymongo import MongoClient
import json
import PhoneTextSender as PTS
 
client = MongoClient("mongodb+srv://saatvik:fuckmylife@cluster0.bak7hv2.mongodb.net/?retryWrites=true&w=majority")

db = client['phonenumbers']
collection = db['numbs']

def count_DB():
    doc_count = collection.count_documents({})
    return doc_count

def add_to_DB(id_num, phone_num, ticker):
    if(collection.find_one({"phonenum":phone_num}) == None):
        post = {"_id": id_num, "phonenum": phone_num, "ticker": ticker}
        collection.insert_one(post)
        return True
    else:
        return False

def update_from_DB(phone, ticker):
    collection.update_one({"phonenum": phone}, {'$set': {"ticker": ticker}})

def remove_from_DB(phone_num):
    collection.find_one_and_delete({"phonenum":phone_num})
    
def send_all(message):
    def helper(string): 
        string = json.dumps(string)
        string = string[len(string)-12 : len(string)-2]
        return string

    for document in collection.find({}):
        PTS.full_Send(message, helper(document))
#send_all(message) <-- message is whatever stock you want to recommend. 