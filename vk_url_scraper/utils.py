import json
import os
import sys
from contextlib import contextmanager
from datetime import datetime


class DateTimeEncoder(json.JSONEncoder):
    # to allow json.dump with datetimes do json.dumps(obj, cls=DateTimeEncoder)
    def default(self, o):
        if isinstance(o, datetime):
            return str(o)  # with timezone
        return json.JSONEncoder.default(self, o)


def captcha_handler(captcha):
    key = input(
        f"CAPTCHA DETECTED, please solve it and input the solution. url={captcha.get_url()}:"
    ).strip()
    return captcha.try_again(key)


@contextmanager
def suppress_stdout():
    # https://thesmithfam.org/blog/2012/10/25/temporarily-suppress-console-output-in-python/
    # this is used to silence ytdlp which does not fully respects quite=True and outputs filenames to the console
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
