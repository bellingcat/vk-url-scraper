import json
import os
import re
import time
from datetime import datetime

import requests


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
        f"""CAPTCHA DETECTED, please solve it and put the solution into the webpage specified in the 'CAPTCHA_HANDLE_URL' env variable in the next 2min. Put the answer in the format "{captcha.sid}=SOLUTION".

    {captcha.sid=}
    {captcha.get_url()=}
    """,
        flush=True,
    )
    if "CAPTCHA_HANDLE_URL" in os.environ:
        url = os.environ["CAPTCHA_HANDLE_URL"]
        regex_string = re.compile(f"{captcha.sid}=(.*)")
        for wait in 24 * [5]:  # tries every 5s for 2min
            print(f"sending request to {url=}", flush=True)
            r = requests.get(url)
            if r.status_code == 200:
                print(f"got response {r.text=}", flush=True)
                if key := regex_string.search(r.text):
                    print(f"got captcha result {key=}", flush=True)
                    return captcha.try_again(key[0])
            print(f"sleeping {wait} seconds", flush=True)
            time.sleep(wait)
    else:
        key = input(f"Enter captcha code for {captcha.get_url()}:").strip()
        return captcha.try_again(key[0])

    return False
