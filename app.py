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
        return render_template('index.html'), 200
    
    else:
        data = request.get_json()
        if data['object'] == 'page':
            sender_id = data['entry'][0]['messaging'][0]['sender']['id']
            messaging_event = data['entry'][0]['messaging'][0]
            
            if collection.count_documents({"_id": sender_id}) > 0:
                
                if messaging_event.get('message'):
                    messaging_text = messaging_event['message']['text'] if 'text' in messaging_event['message'] else 'no text'
                    response = parse_message(messaging_text, sender_id)
                    bot.send_text_message(sender_id, response)

            elif collection.count_documents({"_id": wait_id+sender_id}) > 0:
                bot.send_text_message(sender_id, "Doesn't seem like you've registered yet.\nRegister here: {}/register?key={}".format(app_url, sender_id))
            
            else:
                collection.insert_one({"_id": wait_id+sender_id})
                bot.send_text_message(sender_id, "Hello there, new person!\nRegister here: {}/register?key={}".format(app_url, sender_id))
                return "ok", 200
        
        return "ok", 200


@app.route('/register', methods=['GET', 'POST'])
def new_user_registration():
    
    if request.method == 'GET':
        pk = request.args.get('key')
        app.logger.info('{} is undergoing registration.'.format(pk))
        return render_template('register.html', form=RegisterForm(fb_id=pk), message="") if collection.count_documents({"_id": wait_id+str(pk)}) > 0 else redirect('/')
    
    else:
        fb_id = request.form.get('fb_id')
        gla_id = request.form.get('gla_id')
        gla_pass = request.form.get('gla_pass')
        loginResult = scraper.login(gla_id, gla_pass)
        
        if loginResult == 2:
            form = RegisterForm(fb_id=fb_id)
            app.logger.info('{} provided invalid credentials.'.format(fb_id))
            return render_template('register.html', form=form, message="Invalid credentials.")
        elif loginResult > 2:
            form = RegisterForm(fb_id=fb_id)
            app.logger.info('{} registration threw some error.'.format(fb_id))
            return render_template('register.html', form=form, message="Something went wrong. Try again.")
        
        app.logger.info('{} completed registration.'.format(fb_id))
        collection.insert_one({"_id": fb_id, "guid": gla_id, "thing": f.encrypt(gla_pass.encode()), "loggedIn": 1})
        collection.delete_one({"_id": wait_id+fb_id})
        bot.send_text_message(fb_id, "Alrighty! We can get started. :D")
        return '<h1> Login successful! You can now close this page and chat to the bot. </h1>'


def handle_entity(message, r, alt, except_message):

    if scraper.check_loggedIn(r['guid']):
        bot.send_action(r['_id'], "typing_on")
        parse = witClient.message(message)
        
        try:
            if 'logout' in parse['entities']:
                collection.update_one({"_id": r['_id']}, {'$set': {'loggedIn': 0}})
                app.logger.info('{} logged out.'.format(r['_id']))
                return "Logged out! Goodbye. :)"
            
            elif 'delete_data' in parse['entities']:
                collection.delete_one({"_id": r['_id']})
                app.logger.info('{} deleted their data.'.format(r['_id']))
                return "Deleted! :) "
            
            elif 'datetime' in parse['entities']:
                return scraper.read_date(parse['entities']['datetime'][0]['value'][:10], r['guid'])
            
            elif 'read_next' in parse['entities']:
                return scraper.read_now(r['guid'])
            
            else:
                return alt

        except Exception as e:
            app.logger.info('{} messaged "{}" that threw an error: {}'.format(r['_id'], message, e))
            return except_message
    
    else:
        app.logger.info('{} was logged out.'.format(r['_id']))
        collection.update_one({"_id": r['_id']}, {'$set': {'loggedIn': 0}})
        return parse_message(message, r['_id'])


def parse_message(message, id):
   
    r = collection.find_one({"_id": id})
    
    if r['loggedIn'] == 0:
        bot.send_action(id, "typing_on")
        loginResult = scraper.login(r['guid'], (f.decrypt(r['thing'])).decode())
    
        if loginResult == 1:
            app.logger.info('{} was logged in.'.format(id))
            collection.update_one({"_id": id}, {'$set': {'loggedIn': 1}}) 
        
        else:
            app.logger.info('{} was unable to log in.'.format(id))
            collection.delete_one({"_id": id})
            collection.insert_one({"_id": wait_id+id})
            return "Whoops! Something went wrong; maybe your login details changed?\nRegister here: {}/register?key={}".format(app_url, id)
    
    return handle_entity(message, r, "I can't answer that yet.", "I was unable to understand that. Try again?")


if __name__ == "__main__":
    app.run(debug = True, port = 80)
