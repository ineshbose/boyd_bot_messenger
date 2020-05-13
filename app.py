import os, json
import scraper
from pymessenger import Bot
from cryptography.fernet import Fernet
from flask import Flask, request, redirect, render_template, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired
from pymongo import MongoClient


app = Flask(__name__)                                               # Importing Flask app name
app_url = os.environ.get("APP_URL")                                 # App URL as variable to easily change it
app.config['SECRET_KEY'] = os.environ.get("FLASK_KEY")              # Flask Secret Key to enable FlaskForm
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")             # Facebook Page Access Token
webhook_token = os.environ.get("VERIFY_TOKEN")                      # Webhook Token for GET request
wb_arg_name = os.environ.get("WB_ARG_NAME")                         # Webhook Argument Name
cluster = MongoClient(os.environ.get("MONGO_TOKEN"))                # Mongo Cluster
db = cluster[os.environ.get("FIRST_CLUSTER")]                       # Mongo Database in the Cluster
collection = db[os.environ.get("COLLECTION_NAME")]                  # Mongo Collection in the Database
wait_id = os.environ.get("WAIT_ID")                                 # Prefix ID to distinguish between registered users and in-registration users
f = Fernet(os.environ.get("FERNET_KEY"))                            # Encryption key using Fernet
bot = Bot(PAGE_ACCESS_TOKEN)                                        # Facebook Bot using Page Access Token and pymessenger


class RegisterForm(FlaskForm):
    """Registration form for users.

    Contains 3 essential input fields (+ 1 `SubmitField`).
    """
    fb_id = HiddenField('fb_id')
    gla_id = StringField('GUID', validators=[DataRequired()])
    gla_pass = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


@app.route('/')
def index():
    """Returns index() view for the app.

    Returns
    -------
    template
        The home page for the app corresponding the URL (`app_url`+'/').
    """
    return render_template('index.html')


@app.route('/webhook', methods=['GET','POST'])
def webhook():
    """Enables webhook for the app.

    A method to create GET and POST requests with the app to Dialogflow.
    
    Returns
    -------
    template
        On successful webhook, a template is rendered.

    json
        The response to POST request.
    """
    
    if request.method == 'GET':
        if not request.args.get(wb_arg_name) == webhook_token:
            return "Verification token mismatch", 403
        return render_template('index.html'), 200
    
    else:
        data = request.get_json()

        try:
            sender_id = data['originalDetectIntentRequest']['payload']['data']['sender']['id']
        except KeyError:
            return
        
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
    """Registration for a new user.

    Using `wait_id`, in-registration user is distinguished and then logged in using `scraper.login()` and depending
    on returned boolean value, the page is re-rendered.

    Returns
    -------
    template
        Depending on login, the page is rendered again.
    """
    
    if request.method == 'GET':
        pk = request.args.get('key')
        return render_template('register.html', form=RegisterForm(fb_id=pk), message="") if collection.count_documents({"_id": wait_id+str(pk)}) > 0 else redirect('/')
    
    else:
        fb_id = request.form.get('fb_id')
        gla_id = request.form.get('gla_id')
        gla_pass = request.form.get('gla_pass')
        login_result = scraper.login(gla_id, gla_pass)
        
        if not login_result:
            form = RegisterForm(fb_id=fb_id)
            return render_template('register.html', form=form, message="Invalid credentials.")
        
        collection.insert_one({"_id": fb_id, "guid": gla_id, "gupw": f.encrypt(gla_pass.encode()), "loggedIn": 1})
        collection.delete_one({"_id": wait_id+fb_id})
        bot.send_text_message(fb_id, "Alrighty! We can get started. :D")
        return render_template('register.html', success='Login successful! You can now close this page and chat to the bot.')


def prepare_json(message):
    """Prepares a formatted JSON containing the message.

    To return a message from a POST request, Dialogflow requires a formatted JSON.
    Using `pymessenger` to send messages would not be good practice.

    Parameters
    ----------
    message : str
        The message to return.

    Returns
    -------
    json
        A formatted JSON for Dialogflow with the message.
    """

    res = {
        'fulfillmentText': message,
    }
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def handle_intent(data, r):
    """Checks intent for a message and creates response.

    If an intent is found in a message, a response is returned.

    Parameters
    ----------
    data :
        The JSON of the POST request.
    r :
        The details of the user on Mongo.

    Returns
    -------
    str
        The response if intent is satisfied

    null
        If intent is not handled by the app, Dialogflow creates response.
    """

    if scraper.check_loggedIn(r['guid']):
        bot.send_action(r['_id'], "typing_on")
        intent = data['queryResult']['intent']
        
        try:
            if 'displayName' in intent:
                if intent['displayName'].lower() == 'delete data':
                    collection.delete_one({"_id": r['_id']})
                    return "Deleted! :) "
                
                elif intent['displayName'].lower() == 'read timetable':
                    return scraper.read_date(r['guid'], data['queryResult']['parameters']['date-time'][:10])
                
                elif intent['displayName'].lower() == 'read next':
                    return scraper.read_now(r['guid'])

                else:
                    return
                
            else:
                return

        except Exception as e:
            return "I'm sorry, something went wrong understanding that. :( \n\n\nERROR: {}".format(e)
    
    else:
        collection.update_one({"_id": r['_id']}, {'$set': {'loggedIn': 0}})
        return parse_message(data, r['_id'])


def parse_message(data, uid):
    """Parses the message of the user.

    The main method handling log in and intents for the message.

    Parameters
    ----------
    data :
        The JSON of the POST request.
    uid : str
        The unique ID for the Facebook user of the app.

    Returns
    -------
    str
        A response for the message.

    null
        If intent is not handled by app, the response is created by Dialogflow.
    """
   
    r = collection.find_one({"_id": uid})
    
    if r['loggedIn'] == 0:
        bot.send_action(uid, "typing_on")
        login_result = scraper.login(r['guid'], (f.decrypt(r['gupw'])).decode())
    
        if login_result:
            collection.update_one({"_id": uid}, {'$set': {'loggedIn': 1}}) 
        
        else:
            collection.delete_one({"_id": uid})
            collection.insert_one({"_id": wait_id+uid})
            return "Whoops! Something went wrong; maybe your login details changed?\nRegister here: {}/register?key={}".format(app_url, uid)
    
    return handle_intent(data, r)


if __name__ == "__main__":
    app.run(debug = False, port = 80)
