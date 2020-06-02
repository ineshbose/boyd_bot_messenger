import os, json
import timetable, facebook
from pymongo import MongoClient
from flask_wtf import FlaskForm
from cryptography.fernet import Fernet
from wtforms.validators import DataRequired
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from flask import Flask, request, redirect, render_template, make_response


app = Flask(__name__)
app_url = os.environ["APP_URL"]
app.config['SECRET_KEY'] = os.environ["FLASK_KEY"]
PAGE_ACCESS_TOKEN = os.environ["PAGE_ACCESS_TOKEN"]
webhook_token = os.environ["VERIFY_TOKEN"]
wb_arg_name = os.environ["WB_ARG_NAME"]
cluster = MongoClient(os.environ["MONGO_TOKEN"])
db = cluster[os.environ["FIRST_CLUSTER"]]
collection = db[os.environ["COLLECTION_NAME"]]
wait_id = os.environ["WAIT_ID"]
f = Fernet(os.environ["FERNET_KEY"])


class RegisterForm(FlaskForm):
    fb_id = HiddenField('fb_id')
    gla_id = StringField('GUID', validators=[DataRequired()])
    gla_pass = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/webhook', methods=['POST'])
def webhook():

    if not request.headers.get(wb_arg_name) == webhook_token:
        return "Verification token mismatch", 403

    data = request.get_json()

    # This area is a little delicate. WIP
    try:
        sender_id = data['originalDetectIntentRequest']['payload']['data']['sender']['id']
    except KeyError:
        return
    
    if collection.count_documents({"_id": sender_id}) > 0:
        response = parse_message(data, sender_id)

    elif collection.count_documents({"_id": wait_id+sender_id}) > 0:
        response = "Doesn't seem like you've registered yet.\nRegister here: {}/register?key={}".format(app_url, sender_id)
    
    else:
        user_data = facebook.verify(sender_id, PAGE_ACCESS_TOKEN)
        if 'error' in user_data:
            return
        collection.insert_one({"_id": wait_id+sender_id})
        response = "Hey there, {}! To get started, register here: {}/register?key={}".format(user_data['first_name'], app_url, sender_id)

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
        login_result = timetable.login(gla_id, gla_pass)
        log("{} undergoing registration. Result: {}".format(fb_id, login_result))

        if not login_result:
            form = RegisterForm(fb_id=fb_id)
            return render_template('register.html', form=form, message="Invalid credentials.")
        
        collection.insert_one({"_id": fb_id, "guid": gla_id, "gupw": f.encrypt(gla_pass.encode())})
        collection.delete_one({"_id": wait_id+fb_id})
        facebook.send_message(fb_id, PAGE_ACCESS_TOKEN, "Alrighty! We can get started. :D")        # To alert user on Facebook Messenger. This can be removed.
        return render_template('register.html', success='Login successful! You can now close this page and chat to the bot.')


def prepare_json(message):

    res = { 'fulfillmentText': message, }
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def handle_intent(data, r):

    intent = data['queryResult']['intent']
    
    try:
        if 'displayName' in intent:
            if intent['displayName'].lower() == 'delete data':
                collection.delete_one({"_id": r['_id']})
                return "Deleted! :) "

            elif intent['displayName'].lower() == 'read next':
                return timetable.read_date(r['guid'])
            
            elif intent['displayName'].lower() == 'read timetable':
                return timetable.read_date(r['guid'], data['queryResult']['parameters']['date-time'])

        return

    except Exception as e:
        log("Exception ({}) thrown: {}. {} sent '{}'.".format(type(e).__name__, e, r['_id'], data['queryResult']['queryText']))
        return "I'm sorry, something went wrong understanding that. :("


def parse_message(data, uid):

    r = collection.find_one({"_id": uid})
    
    if not timetable.check_loggedIn(r['guid']):
        log("{} logging in again.".format(uid))
        login_result = timetable.login(r['guid'], (f.decrypt(r['gupw'])).decode())
    
        if not login_result:
            log("{} failed to log in.".format(uid))
            collection.delete_one({"_id": uid})
            collection.insert_one({"_id": wait_id+uid})
            return "Whoops! Something went wrong; maybe your login details changed?\nRegister here: {}/register?key={}".format(app_url, uid)
    
    return handle_intent(data, r)


def log(message):
    print(message)          # print() is not good practice. Will be replaced.


if __name__ == "__main__":
    app.run(debug = False, port = 80)
