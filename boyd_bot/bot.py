from flask import request, redirect, render_template, url_for, abort, current_app
from boyd_bot.forms import RegisterForm

def bot_functions(config, webhook_token, wb_arg_name, timetable, guard, db, parser, platform):

    def webhook():

        if request.method == "GET":
            return redirect(url_for("boyd_bot.index"))

        if not (
            guard.sanitized(request.headers, wb_arg_name, webhook_token)
            or guard.sanitized(request.args, wb_arg_name, webhook_token)
        ):
            abort(403)

        request_data = request.get_json()
        sender_id, platform_user = platform.get_id(request_data)

        if db.check_registered(sender_id):
            response = user_gateway(request_data, sender_id)

        elif db.check_in_reg(sender_id):
            response = config["MSG"]["NOT_REG"](db.get_data(sender_id)["reg_id"])

        else:
            user_data = platform.get_user_data(sender_id)
            if (
                not sender_id
                or (not platform.validate_user(user_data) and platform_user)
                or not (platform_user or config["FEATURES"]["DEMO"])
            ):
                current_app.logger.warn(config["LOG"]["INVALID_USER"](sender_id))
                abort(401)

            reg_id = db.insert_in_reg(sender_id, platform_user)
            response = config["MSG"]["NEW_USER"](
                user_data.get("first_name", "new person"), reg_id
            )

        return platform.reply(response)


    def new_user_registration(reg_id):

        if request.method == "GET":
            return (
                render_template(
                    config["TEMPLATES"]["REG_FORM"],
                    allow_remember=db.get_data(reg_id)["platform_user"],
                    form=RegisterForm(reg_id=reg_id),
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
            subscribe = request.form.getlist("subscribe")

            remember = (
                request.form.get("remember")
                if config["FEATURES"]["ONE_TIME_USE"]
                else db.get_data(reg_id)["platform_user"]
            )

            uid = db.get_data(reg_id)["user_id"]
            login_result = timetable.login(uid, uni_id, uni_pw)
            current_app.logger.info(config["LOG"]["USER_AUTH"](uid, login_result))

            if not login_result[0]:
                return render_template(
                    config["TEMPLATES"]["REG_FORM"],
                    allow_remember=db.get_data(reg_id)["platform_user"],
                    form=RegisterForm(reg_id=reg_id),
                    message=login_result[1],
                )

            db.delete_data(uid)
            db.delete_data(reg_id)
            user_details = (
                {"uni_id": uni_id, "uni_pw": uni_pw, "subscribe": subscribe}
                if remember
                else {}
            )
            db.insert_data(uid, **user_details)
            platform.send_message(uid, config["MSG"]["REG_ACKNOWLEDGE"])

            return render_template(config["TEMPLATES"]["REG_FORM"], success=True)


    def user_gateway(request_data, uid):

        try:

            if not timetable.check_loggedIn(uid):

                user_data = db.get_data(uid)
                current_app.logger.info(config["LOG"]["RELOGIN"](uid))

                if not guard.sanitized(user_data, ["uni_id", "uni_pw"]):
                    db.delete_data(uid)
                    return config["MSG"]["ONE_TIME_DONE"]

                login_result = timetable.login(
                    user_data["_id"], user_data["uni_id"], user_data["uni_pw"]
                )

                if not login_result[0]:

                    current_app.logger.warn(config["LOG"]["AUTH_FAIL"](uid, login_result))
                    db.delete_data(uid)
                    reg_id = db.insert_in_reg(*platform.get_id(request_data))

                    return config["MSG"]["ERROR_LOGIN"](reg_id)

            message = parser.parse(request_data, uid)

        except Exception as e:
            current_app.logger.exception(config["LOG"]["ERROR"](type(e).__name__, e, uid, request_data))
            message = config["MSG"]["ERROR_MSG"]

        return message

    return webhook, new_user_registration
