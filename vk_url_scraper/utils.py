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
