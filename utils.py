from flask import request, abort
from functools import wraps
import random
import string


def gen_random_str(length: int = 12) -> str:
    return "".join([random.choice(string.ascii_letters) for i in range(length)])


def auth_only(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        if not request.user:
            abort(403)
        return view_function(*args, **kwargs)

    return wrapper
