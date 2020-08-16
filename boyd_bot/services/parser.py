from .. import db, timetable


class Parser:
    """
    Breaks down data to get information,
    trigger events and generate a response.
    """

    def __init__(self):
        """
        Initialise class with required fields (if any).
        """
        pass

    def help_text(self):
        """
        Returns message for "help_text" intent.
        """
        return (
            "I'm your university chatbot, so you can ask me "
            "(almost) anything regarding your timetable!\n"
            "For example, 'classes today', 'do I have psychology tomorrow?', "
            "'march 3rd'.\n\nIf you want, you can stop using my help and "
            "have your data deleted by saying 'delete data' "
            "but I don't want you to go! You'll always be welcome back. :)"
        )

    def delete_data(self, uid):
        """
        Returns response for "delete_data" intent.
        """
        return (
            "Deleted! :)"
            if db.delete_data(uid)
            else "Something went wrong. :("
        )

    def read_timetable(self, uid, data):
        """
        Returns message for "read_timetable" intent.
        """
        param = data["queryResult"]["parameters"]
        dt_param = param["date-time"]

        param_keys = {
            "date_time": ["date_time"],
            "startDateTime": ["startDateTime", "endDateTime"],
            "startDate": ["startDate", "endDate"],
            "startTime": ["startTime", "endTime"],
        }

        message = []
        args = []

        if not dt_param:
            args.extend([None, None])
            args.append(param.get("class-name"))
            message.extend(timetable.read(uid, *args))

        else:

            for s_dt in dt_param:
                args.clear()

                for p_key in param_keys:
                    if p_key in s_dt:
                        dt_keys = param_keys[p_key]
                        args.extend(
                            [
                                s_dt[dt_keys[0]],
                                s_dt[dt_keys[1]]
                                if len(dt_keys) > 1 else None,
                            ]
                        )
                        break

                if not args:
                    dt_val = (
                        f"{s_dt[:10]}T00:00:00{s_dt[19:len(s_dt)]}"
                    )
                    args.extend([dt_val, None])

                args.append(param.get("class-name"))
                message.extend(timetable.read(uid, *args))

        return message

    def parse(self, request_data, uid):
        """
        Breaks down data to determine intent and generate a response.
        """
        message_text = request_data["queryResult"].get("queryText")
        intent = request_data["queryResult"].get("intent")
        default_reply = None

        if not intent:
            return default_reply

        intent_name = intent["displayName"].lower().replace(" ", "_")
        intent_linking = {
            "delete_data": lambda: self.delete_data(uid),
            "read_timetable": lambda: self.read_timetable(uid, request_data),
            "help_text": self.help_text,
        }

        return (
            intent_linking[intent_name]()
            if intent_name in intent_linking
            else default_reply
        )
