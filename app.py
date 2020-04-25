import os, sys, json
import scraper
from pymessenger import Bot
from cryptography.fernet import Fernet
from flask import Flask, request, session, redirect, render_template, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired
from pymongo import MongoClient


app = Flask(__name__)
app_url = os.environ.get("APP_URL")
app.config['SECRET_KEY'] = os.environ.get("FLASK_KEY")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
webhook_token = os.environ.get("VERIFY_TOKEN")
wb_arg_name = os.environ.get("WB_ARG_NAME")
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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/webhook', methods=['GET','POST'])
def webhook():
    
    if request.method == 'GET':
        if not request.args.get(wb_arg_name) == webhook_token:
            return "Verification token mismatch", 403
        return render_template('index.html'), 200
    
    else:
        data = request.get_json()
        sender_id = data['originalDetectIntentRequest']['payload']['data']['sender']['id']
        
        if collection.count_documents({"_id": sender_id}) > 0:
            response = parse_message(data, sender_id)

        elif collection.count_documents({"_id": wait_id+sender_id}) > 0:
            response = "Doesn't seem like you've registered yet.\nRegister here: {}/register?key={}".format(app_url, sender_id)
        
        else:
            collection.insert_one({"_id": wait_id+sender_id})
            response = "Hello there, new person!\nRegister here: {}/register?key={}".format(app_url, sender_id)
    
        return prepare_json(response)


@app.route('/register', methods=['GET', 'POST'])
def new_user_registration():
    
    if request.method == 'GET':
        pk = request.args.get('key')
        return render_template('register.html', form=RegisterForm(fb_id=pk), message="") if collection.count_documents({"_id": wait_id+str(pk)}) > 0 else redirect('/')
    
    else:
        fb_id = request.form.get('fb_id')
        gla_id = request.form.get('gla_id')
        gla_pass = request.form.get('gla_pass')
        loginResult = scraper.login(gla_id, gla_pass)
        
        if loginResult == 2:
            form = RegisterForm(fb_id=fb_id)
            return render_template('register.html', form=form, message="Invalid credentials.")
        elif loginResult > 2:
            form = RegisterForm(fb_id=fb_id)
            return render_template('register.html', form=form, message="Something went wrong. Try again.")
        
        collection.insert_one({"_id": fb_id, "guid": gla_id, "thing": f.encrypt(gla_pass.encode()), "loggedIn": 1})
        collection.delete_one({"_id": wait_id+fb_id})
        bot.send_text_message(fb_id, "Alrighty! We can get started. :D")
        return '<h1> Login successful! You can now close this page and chat to the bot. </h1>'


def prepare_json(message):
    res = {
        'fulfillmentText': message,
    }
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def handle_intent(data, r):

    if scraper.check_loggedIn(r['guid']):
        bot.send_action(r['_id'], "typing_on")
        intent = data['queryResult']['intent']
        
        try:
            if 'displayName' in intent:
                if intent['displayName'] == 'Default Welcome Intent':
                    return

                if intent['displayName'] == 'delete data':
                    collection.delete_one({"_id": r['_id']})
                    return "Deleted! :) "
                
                elif intent['displayName'] == 'read timetable':
                    print(data['queryResult']['parameters']['date-time'][:10])
                    return scraper.read_date(data['queryResult']['parameters']['date-time'][:10], r['guid'])
                
                elif intent['displayName'] == 'read next':
                    return scraper.read_now(r['guid'])

                else:
                    return "I'm unable to answer that."
                
            else:
                return

        except:
            return "I'm sorry, something went wrong understanding that. :("
    
    else:
        collection.update_one({"_id": r['_id']}, {'$set': {'loggedIn': 0}})
        return parse_message(data, r['_id'])


def parse_message(data, id):
   
    r = collection.find_one({"_id": id})
    
    if r['loggedIn'] == 0:
        bot.send_action(id, "typing_on")
        loginResult = scraper.login(r['guid'], (f.decrypt(r['thing'])).decode())
    
        if loginResult == 1:
            collection.update_one({"_id": id}, {'$set': {'loggedIn': 1}}) 
        
        else:
            collection.delete_one({"_id": id})
            collection.insert_one({"_id": wait_id+id})
            return "Whoops! Something went wrong; maybe your login details changed?\nRegister here: {}/register?key={}".format(app_url, id)
    
    return handle_intent(data, r)


if __name__ == "__main__":
    app.run(debug = True, port = 80)