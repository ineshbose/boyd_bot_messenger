import os, sys
import scraper
from pymessenger import Bot
from cryptography.fernet import Fernet
from flask import Flask, request, session, redirect
from pymongo import MongoClient
from wit import Wit


app = Flask(__name__)
witClient = Wit(os.environ.get("WIT_ACCESS_TOKEN"))
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
cluster = MongoClient(os.environ.get("MONGO_TOKEN"))
db = cluster[os.environ.get("FIRST_CLUSTER")]
collection = db[os.environ.get("COLLECTION_NAME")]


file = open(os.environ.get("KEY_NAME"), 'rb')
key = file.read()
file.close()
f = Fernet(key)


bot = Bot(PAGE_ACCESS_TOKEN)


@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ.get("VERIFY_TOKEN"):
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello World", 200


@app.route('/', methods=['POST'])
def webhook():
    
    data = request.get_json()
    
    if data['object'] == 'page':
        for entry in data['entry']:
            
            for messaging_event in entry['messaging']:
                sender_id = messaging_event['sender']['id']
                
                if collection.find({"_id": sender_id}).count()==0 and collection.find({"_id": "W"+sender_id}).count()==0:
                    bot.send_text_message(sender_id, "New user! Enter your GUID.")
                    collection.insert({"_id": "W"+sender_id, "guid": "", "thing": "", "expect":{"expecting_guid": 1, "expecting_pass": 0}})
                    return "ok", 200
                
                if collection.find({"_id": "W"+sender_id}).count()>0:
                    result = collection.find_one({"_id": "W"+sender_id})
                    if result['expect']['expecting_guid'] == 1:
                
                        try:
                            if type(int(messaging_event['message']['text'][:7])) == type(123) and type(messaging_event['message']['text'][7]) == type("a") and len(messaging_event['message']['text']) == 8:
                                collection.update_one({"_id": "W"+sender_id}, {'$set': {"guid": messaging_event['message']['text'], "expect":{"expecting_guid": 0, "expecting_pass": 1}}})
                                bot.send_text_message(sender_id, "Enter password (No one will see it and you can delete it afterwards :) ).")
                                return "ok", 200
                            else:
                                bot.send_text_message(sender_id, "Invalid GUID. It is seven integers with your surname's initial. Enter it again.")
                                return "ok", 200
                
                        except:
                            bot.send_text_message(sender_id, "Invalid GUID. It is seven integers with your surname's initial. Enter it again.")
                            return "ok", 200
                
                    elif result['expect']['expecting_pass'] == 1:
                        bot.send_text_message(sender_id, "Attempting to log you in..")
                        bot.send_action(sender_id, "typing_on")
                        loginResult = scraper.login(result['guid'], messaging_event['message']['text'])
                
                        if loginResult == 1:
                            bot.send_text_message(sender_id, "Logged in!")
                            collection.insert({"_id": sender_id, "guid": result['guid'], "thing": f.encrypt(messaging_event['message']['text'].encode()), "loggedIn": 1})
                            collection.delete_one({"_id": "W"+sender_id})
                            return "ok", 200
                
                        elif loginResult == 2:
                            bot.send_text_message(sender_id, "Invalid credentials. Enter GUID again.")
                            collection.update_one(
                            {"_id": "W"+sender_id}, 
                            {'$set': {"guid": "", "thing": "", "expect":{"expecting_guid": 1, "expecting_pass": 0}}})
                            return "ok", 200
                
                        elif loginResult == 3:
                            bot.send_text_message(sender_id, "Something went wrong. Maybe the connection was too slow. Enter GUID again.")
                            collection.update_one(
                            {"_id": "W"+sender_id}, 
                            {'$set': {"guid": "", "thing": "", "expect":{"expecting_guid": 1, "expecting_pass": 0}}})
                            return "ok", 200
                
                if messaging_event.get('message'):
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:
                        messaging_text = 'no text'
                
                    response = parse_message(messaging_text, sender_id)
                    bot.send_text_message(sender_id, response)
    
    return "ok", 200


def parse_message(message, id):
   
    r = collection.find_one({"_id": id})
    
    if r['loggedIn'] == 0:
        bot.send_text_message(id, "Logging in..")
        bot.send_action(id, "typing_on")
        loginResult = scraper.login(r['guid'], (f.decrypt(r['thing'])).decode())
    
        if loginResult == 1:
            collection.update_one({"_id": id}, {'$set': {'loggedIn': 1}}) 
            bot.send_text_message(id, "Logged in!")
            
            try:
                parse = witClient.message(message)
                bot.send_action(id, "typing_on")
                return scraper.specific_day(parse['entities']['datetime'][0]['value'][:10], r['guid'])
            except:
                return "What's up?"
        
        else:
            collection.delete_one({"_id": id})
            collection.insert({"_id": "W"+id, "guid": "", "thing": "", "expect":{"expecting_guid": 1, "expecting_pass": 0}})
            return "Something went wrong. Enter GUID."   
    
    else:
    
        if scraper.check_browser(r['guid']):
            if message.lower() == "logout":
                scraper.close(r['guid'])
                collection.update_one({"_id": id}, {'$set': {'loggedIn': 0}})
                return "Logged out! Goodbye. :)"
            elif message.lower() == "delete data":
                collection.delete_one({"_id": id})
                return "Deleted! :) "
            
            else:
                
                try:
                    parse = witClient.message(message)
                    bot.send_action(id, "typing_on")
                    return scraper.specific_day(parse['entities']['datetime'][0]['value'][:10], r['guid'])
                
                except:
                    return "Not sure how to answer that."
        
        else:
            collection.update_one({"_id": id}, {'$set': {'loggedIn': 0}})
            return "You have been logged out due to some error or being idle for too long. Say hello to log in again. :) "


if __name__ == "__main__":
    app.run(debug = True, port = 80)