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
platform = Platform(platform_token=os.environ["PLATFORM_TOKEN"])
db = Database(
    db_token=os.environ["DB_MAIN_TOKEN"],
    key1=os.environ["DB_KEY1"],
    key2=os.environ["DB_KEY2"],
)
parser = Parser()
guard = Guard(key=os.environ["GUARD_KEY"])


@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    if request.method == "GET":
        return redirect("/")

    if not request.headers.get(wb_arg_name) == webhook_token:
        return "Authorisation Failed", 403

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
        ).format(app_url, db.get_reg_id(sender_id))

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

        if not guard.sanitized(request.args, "id", db):
            return redirect("/")

        reg_id = request.args.get("id")
        return render_template("register.html", form=RegisterForm(reg_id=reg_id))

    else:

        if not guard.sanitized(request.form, ["reg_id", "uni_id", "uni_pw"], db):
            return redirect("/")

        reg_id = request.form.get("reg_id")
        uni_id = request.form.get("uni_id")
        uni_pw = request.form.get("uni_pw")

        uid = db.get_user_id(reg_id)
        login_result = timetable.login(uid, uni_id, uni_pw)
        log("{} undergoing registration. Result: {}".format(uid, login_result))

        if not login_result[0]:
            return render_template(
                "register.html",
                form=RegisterForm(reg_id=reg_id),
                message=login_result[1],
            )

        db.delete_data(uid)
        db.insert_data(uid, guard.encrypt(uni_id), guard.encrypt(uni_pw))
        platform.send_message(uid, "Alrighty! We can get started. :D")

        return render_template(
            "register.html",
            success="Login successful! You can now close this page and chat to the bot.",
        )


def user_gateway(request_data, uid):

    try:
        user_data = db.get_data(uid)

        if not timetable.check_loggedIn(user_data["_id"]):

            log("{} logging in again.".format(uid))

            login_result = timetable.login(
                user_data["_id"],
                guard.decrypt(user_data["uni_id"]),
                guard.decrypt(user_data["uni_pw"]),
            )

            if not login_result[0]:

                log("{} failed to log in. Result: {}".format(uid, login_result))
                db.delete_data(uid)

                hash_id = guard.sha256(uid)
                reg_id = (
                    hash_id[:15] if not db.check_reg_data(hash_id[:15]) else hash_id
                )
                db.insert_in_reg(uid, reg_id)

                return (
                    "Whoops! Something went wrong; maybe your login details changed?\n"
                    "Register here: {}/register?id={}"
                ).format(app_url, reg_id)

        message = parser.parse(request_data, uid, db)

    except Exception as e:
        log(
            "Exception ({}) thrown: {}. {} requested '{}'.".format(
                type(e).__name__, e, uid, request_data
            )
        )
        message = "I'm sorry, something went wrong understanding that. :("

    return message


def log(message):
    app.logger.info(message)


if __name__ == "__main__":
    app.run(debug=False, port=80)
