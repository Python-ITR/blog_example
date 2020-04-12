import os
import hmac
import random
import string

from functools import wraps

from flask import abort, request


def gen_random_str(length: int = 12) -> str:
    return "".join([random.choice(string.ascii_letters) for i in range(length)])

def get_password_hash(password: str):
    salt: str = os.environ.get("SECRET_KEY", "")
    return hmac.new(salt.encode(), password.encode(), "md5").hexdigest()
