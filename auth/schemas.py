from cerberus import Validator

user_credentials_schema = Validator(
    {
        "username": {"type": "string", "minlength": 4, "regex": "^[a-zA-Z0-9]+$"},
        "password": {"type": "string", "minlength": 6},
    }
)

user_passwd_schema = Validator(
    {
        "password": {"type": "string", "minlength": 6}
    }
)