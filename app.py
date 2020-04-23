import os, sys
import scraper
from pymessenger import Bot
from cryptography.fernet import Fernet
from flask import Flask, request, session, redirect, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired
from pymongo import MongoClient
from wit import Wit


app = Flask(__name__)
app_url = os.environ.get("APP_URL")
app.config['SECRET_KEY'] = os.environ.get("FLASK_KEY")
witClient = Wit(os.environ.get("WIT_ACCESS_TOKEN"))
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
fb_verify = os.environ.get("VERIFY_TOKEN")
cluster = MongoClient(os.environ.get("MONGO_TOKEN"))
db = cluster[os.environ.get("FIRST_CLUSTER")]
collection = db[os.environ.get("COLLECTION_NAME")]
wait_id = os.environ.get("WAIT_ID")
f = Fernet(os.environ.get("FERNET_KEY"))


bot = Bot(PAGE_ACCESS_TOKEN)


class RegisterForm(FlaskForm):
    fb_id = HiddenField('fb_id')
    gla_id = StringField('GUID', validators=[DataRequired()])
    gla_pass = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


@app.route('/', methods=['GET','POST'])
def main():
    
    if request.method == 'GET':
        if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
            if not request.args.get("hub.verify_token") == fb_verify:
                return "Verification token mismatch", 403
            return request.args["hub.challenge"], 200
        return "Hello World", 200
    
    else:
        data = request.get_json()
        if data['object'] == 'page':
            sender_id = data['entry'][0]['messaging'][0]['sender']['id']
            messaging_event = data['entry'][0]['messaging'][0]
            
            if collection.count_documents({"_id": sender_id}) > 0:
                if messaging_event.get('message'):
                    
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    
                    else:
                        messaging_text = 'no text'
                    response = parse_message(messaging_text, sender_id)
                    bot.send_text_message(sender_id, response)

            elif collection.count_documents({"_id": wait_id+sender_id}) > 0:
                bot.send_text_message(sender_id, "Doesn't seem like you've registered yet.\nRegister here: {}/register?key={}".format(app_url, sender_id))
            
            else:
                collection.insert_one({"_id": wait_id+sender_id})
                bot.send_text_message(sender_id, "New user!\nRegister here: {}/register?key={}".format(app_url, sender_id))
                return "ok", 200
        
        return "ok", 200

@app.route('/register', methods=['GET', 'POST'])
def new_user_registration():
    
    if request.method == 'GET':
        pk = request.args.get('key')
        
        if collection.count_documents({"_id": wait_id+str(pk)}) > 0:
            form = RegisterForm(fb_id=pk)
            return render_template('register.html', form=form, message="")
        else:
            return '404'
    
    else:
        fb_id = request.form.get('fb_id')
        gla_id = request.form.get('gla_id')
        gla_pass = request.form.get('gla_pass')
        loginResult = scraper.login(gla_id, gla_pass)
        
        if loginResult == 2:
            form = RegisterForm(fb_id=fb_id)
            return render_template('register.html', form=form, message="Invalid credentials.")
        elif loginResult == 3:
            form = RegisterForm(fb_id=fb_id)
            return render_template('register.html', form=form, message="Something went wrong. Try again.")
        
        collection.insert_one({"_id": fb_id, "guid": gla_id, "thing": f.encrypt(gla_pass.encode()), "loggedIn": 1})
        collection.delete_one({"_id": wait_id+fb_id})
        return '<h1> Login successful! You can now close this page and chat to the bot. </h1>'


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
                
                if 'datetime' in parse['entities']:
                    return scraper.read_date(parse['entities']['datetime'][0]['value'][:10], r['guid'])
                
                elif 'read_next' in parse['entities']:
                    return scraper.read_now(r['guid'])
                
                else:
                    return "What's up?"
            
            except:
                return "So, what's up?"
        
        else:
            collection.delete_one({"_id": id})
            collection.insert_one({"_id": wait_id+id})
            return "Something went wrong.\nRegister here: {}/register?key={}".format(app_url, id)
    
    else:
    
        if scraper.check_loggedIn(r['guid']):
            try:
                parse = witClient.message(message)
                bot.send_action(id, "typing_on")

                if 'logout' in parse['entities']:
                    collection.update_one({"_id": id}, {'$set': {'loggedIn': 0}})
                    return "Logged out! Goodbye. :)"
                
                elif 'delete_data' in parse['entities']:
                    collection.delete_one({"_id": id})
                    return "Deleted! :) "
                
                elif 'datetime' in parse['entities']:
                    return scraper.read_date(parse['entities']['datetime'][0]['value'][:10], r['guid'])
                
                elif 'read_next' in parse['entities']:
                    return scraper.read_now(r['guid'])
                
                else:
                    return "Not sure how to answer that."
            
            except:
                return "Something went wrong with parsing that. Try again."
        
        else:
            collection.update_one({"_id": id}, {'$set': {'loggedIn': 0}})
            return "You have been logged out due to some error or being idle for too long. Say hello to log in again. :) "


if __name__ == "__main__":
    app.run(debug = True, port = 80)