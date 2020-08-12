from flask import request, redirect, render_template, url_for, abort
from . import *


@blueprint.route("/webhook", methods=["GET", "POST"])
def webhook():

    if request.method == "GET":
        return redirect(url_for(".index"))

    if not guard.sanitized([request.headers, request.args], wb_arg_name, webhook_token):
        abort(403)

    request_data = request.get_json()
    sender_id, platform_user = platform.get_id(request_data)

    if db.check_registered(sender_id):
        response = user_gateway(request_data, sender_id)

    elif db.check_in_reg(sender_id):
        response = (
            "It doesn't seem like you've registered yet.\n"
            "Register here: {}/register/{}"
        ).format(app_url, db.get_reg_id(sender_id))

    else:
        user_data = platform.get_user_data(sender_id)
        if (
            not sender_id
            or ("error" in user_data and platform_user)
            or not (platform_user or app.config["FEATURES"]["DEMO"])
        ):
            log("{} is not a valid user".format(sender_id))
            abort(401)

        reg_id = db.insert_in_reg(sender_id, platform_user)
        response = (
            "Hey there, {}! I'm Boyd Bot - your university chatbot, here to make things easier. "
            "To get started, register here: {}/register/{}"
        ).format(user_data.get("first_name", "new person"), app_url, reg_id)

    return platform.reply(response)


@blueprint.route("/register/<reg_id>", methods=["GET", "POST"])
def new_user_registration(reg_id):

    if request.method == "GET":
        return (
            render_template(
                app.config["TEMPLATES"]["REG_FORM"],
                form=RegisterForm(reg_id=reg_id, remember=db.get_reg_id_result(reg_id)),
            )
            if db.get_data(reg_id)
            else abort(404)
        )

    else:

        if not (
            guard.sanitized(request.form, ["reg_id", "uni_id", "uni_pw"])
            and db.get_data(reg_id)
        ):
            abort(400)

        reg_id = request.form.get("reg_id")
        uni_id = request.form.get("uni_id")
        uni_pw = request.form.get("uni_pw")
        subscribe = request.form.get("subscribe")
        
        remember = (
            request.form.get("remember")
            if app.config["FEATURES"]["ONE_TIME_USE"]
            else db.get_reg_id_result(reg_id)
        )

        uid = db.get_user_id(reg_id)
        login_result = timetable.login(uid, uni_id, uni_pw)
        log("{} undergoing registration. Result: {}".format(uid, login_result))

        if not login_result[0]:
            return render_template(
                app.config["TEMPLATES"]["REG_FORM"],
                form=RegisterForm(reg_id=reg_id, remember=remember),
                message=login_result[1],
            )

        db.delete_data(uid)
        db.delete_data(reg_id)
        user_details = {"uni_id": uni_id, "uni_pw": uni_pw} if remember else {}
        user_details["subscribe"] = subscribe
        db.insert_data(uid, **user_details)
        platform.send_message(uid, app.config["MSG"]["REG_ACKNOWLEDGE"])

        return render_template(app.config["TEMPLATES"]["REG_FORM"], success=True)


def user_gateway(request_data, uid):

    try:
        user_data = db.get_data(uid)

        if not timetable.check_loggedIn(user_data["_id"]):

            log("{} logging in again.".format(uid))

            if not guard.sanitized(user_data, ["uni_id", "uni_pw"]):
                db.delete_data(uid)
                return app.config["MSG"]["ONE_TIME_DONE"]

            login_result = timetable.login(
                user_data["_id"], user_data["uni_id"], user_data["uni_pw"]
            )

            if not login_result[0]:

                log("{} failed to log in. Result: {}".format(uid, login_result))
                db.delete_data(uid)
                reg_id = db.insert_in_reg(uid)

                return (
                    "Whoops! Something went wrong; maybe your login details changed?\n"
                    "Register here: {}/register/{}"
                ).format(app_url, reg_id)

        message = parser.parse(request_data, uid)

    except Exception as e:
        log(
            "Exception ({}) thrown: {}. {} requested '{}'.".format(
                type(e).__name__, e, uid, request_data
            )
        )
        message = app.config["MSG"]["ERROR_MSG"]

    return message
