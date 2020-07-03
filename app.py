import timetable
import os, logging
from views import pages, RegisterForm
from services import Platform, Database, Parser, Guard
from flask import Flask, request, redirect, render_template


app = Flask(__name__)
app.register_blueprint(pages)
app.logger.setLevel(logging.DEBUG)

app_url = os.environ["APP_URL"]
app.config["SECRET_KEY"] = os.environ["FLASK_KEY"]
webhook_token = os.environ["VERIFY_TOKEN"]
wb_arg_name = os.environ["WB_ARG_NAME"]
platform = Platform(access_token=os.environ["PAGE_ACCESS_TOKEN"])
db = Database(
    cluster=os.environ["MONGO_TOKEN"],
    db=os.environ["FIRST_CLUSTER"],
    collection=os.environ["COLLECTION_NAME"],
)
parser = Parser()
guard = Guard(key=os.environ["FERNET_KEY"])


@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    if request.method == "GET":
        return redirect("/")

    if not request.headers.get(wb_arg_name) == webhook_token:
        return "Verification token mismatch", 403

    request_data = request.get_json()
    sender_id = platform.get_id(request_data)

    if not sender_id:
        return platform.reply("Hello, developer.")

    if db.check_registered(sender_id):
        response = user_gateway(request_data, sender_id)

    elif db.check_in_reg(sender_id):
        response = (
            "It doesn't seem like you've registered yet.\n"
            "Register here: {}/register?id={}"
        ).format(app_url, db.get_data(sender_id)["reg_id"])

    else:
        user_data = platform.get_user_data(sender_id)
        if "error" in user_data:
            return log("{} is not a valid user".format(sender_id))

        hash_id = guard.sha256(sender_id)
        reg_id = hash_id[:15] if not db.check_reg_data(hash_id[:15]) else hash_id
        db.insert_in_reg(sender_id, reg_id)

        response = (
            "Hey there, {}! I'm Boyd Bot - your university chatbot, here to make things easier. "
            "To get started, register here: {}/register?id={}"
        ).format(user_data["first_name"], app_url, reg_id)

    return platform.reply(response)


@app.route("/register", methods=["GET", "POST"])
def new_user_registration():

    if request.method == "GET":

        if "id" not in request.args:
            return redirect("/")

        reg_id = request.args.get("id")
        return (
            render_template(
                "register.html", form=RegisterForm(reg_id=reg_id), message=""
            )
            if db.check_reg_data(reg_id)
            else redirect("/")
        )

    else:
        reg_id = request.form.get("reg_id")
        uni_id = request.form.get("uni_id")
        uni_pw = request.form.get("uni_pw")
        uid = db.get_user_id(reg_id)
        login_result = timetable.login(uid, uni_id, uni_pw)
        log("{} undergoing registration. Result: {}".format(uid, login_result))

        if not login_result:
            return render_template(
                "register.html",
                form=RegisterForm(reg_id=reg_id),
                message="Invalid credentials.",
            )

        db.delete_in_reg(uid, reg_id)
        db.insert_data(uid, guard.encrypt(uni_id), guard.encrypt(uni_pw))
        platform.send_message(uid, "Alrighty! We can get started. :D")
        return render_template(
            "register.html",
            success="Login successful! You can now close this page and chat to the bot.",
        )


def handle_intent(request_data, uid):

    intent = request_data["queryResult"]["intent"]

    try:

        if "displayName" not in intent:
            return

        intent_name = intent["displayName"].lower()
        intent_linking = {
            "delete data": lambda: parser.delete_data(uid, db),
            "read timetable": lambda: parser.read_timetable(uid, request_data),
        }

        return intent_linking[intent_name]() if intent_name in intent_linking else None

    except Exception as e:
        log(
            "Exception ({}) thrown: {}. {} sent '{}'.".format(
                type(e).__name__, e, uid, request_data["queryResult"]["queryText"]
            )
        )
        return "I'm sorry, something went wrong understanding that. :("


def user_gateway(request_data, uid):

    user_data = db.get_data(uid)

    if not timetable.check_loggedIn(user_data["_id"]):
        log("{} logging in again.".format(uid))
        login_result = timetable.login(
            user_data["_id"],
            guard.decrypt(user_data["uni_id"]),
            guard.decrypt(user_data["uni_pw"]),
        )

        if not login_result:

            log("{} failed to log in.".format(uid))
            db.delete_data(uid)
            hash_id = guard.sha256(uid)
            reg_id = hash_id[:15] if not db.check_reg_data(hash_id[:15]) else hash_id
            db.insert_in_reg(uid, reg_id)

            return (
                "Whoops! Something went wrong; maybe your login details changed?\n"
                "Register here: {}/register?id={}"
            ).format(app_url, reg_id)

    return handle_intent(request_data, uid)


def log(message):
    app.logger.info(message)


if __name__ == "__main__":
    app.run(debug=False, port=80)
