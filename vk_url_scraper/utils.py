import json
import os
from datetime import datetime


class DateTimeEncoder(json.JSONEncoder):
    # to allow json.dump with datetimes do json.dumps(obj, cls=DateTimeEncoder)
    def default(self, o):
        if isinstance(o, datetime):
            return str(o)  # with timezone
        return json.JSONEncoder.default(self, o)


def mkdir_if_not_exists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def captcha_handler(captcha):
    print(
        f"CAPTCHA DETECTED, please solve it and input the solution. {captcha.sid=} {captcha.get_url()=}",
        flush=True,
    )
    key = input(f"Enter captcha code for {captcha.get_url()}:").strip()
    return captcha.try_again(key)
