import sys
import argparse
import json
import dotenv

from services import UsersService
from auth.schemas import user_credentials_schema, user_passwd_schema

dotenv.load_dotenv()

def create_user(args):
    if not user_credentials_schema.validate(
        {"username": args.username, "password": args.password}
    ):
        print("Invalid data. errors: ", json.dumps(user_credentials_schema.errors))
        return
    created_user = UsersService.create_user(args.username, args.password)
    print(f"New user; username: {created_user.username}")


def change_password(args):
    if not user_passwd_schema.validate({"password": args.password}):
        print("Invalid data. errors: ", json.dumps(user_credentials_schema.errors))
        return
    if args.password != args.password_confirm:
        print("Пароли должны совпадать")
        return
    user = UsersService.get_user_by_username(args.username)
    if not user:
        print("И что это за пользователь!? Такого нет!")
        return
    user = UsersService.change_user_password(user.username, args.password)
    print(f"Password is changed to {args.password};")


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="sub-command help")

    # CREATE USER
    create_user_parser = subparsers.add_parser("create_user")
    create_user_parser.add_argument(
        "--username", type=str, help="Username для нового пользователя"
    )
    create_user_parser.add_argument(
        "--password", type=str, help="Password для нового пользователя"
    )
    create_user_parser.set_defaults(func=create_user)

    # CHANGE PASSWORD
    change_password_parser = subparsers.add_parser("change_password")
    change_password_parser.add_argument(
        "--username", type=str, help="Username для нового пользователя"
    )
    change_password_parser.add_argument(
        "--password", type=str, help="Password для нового пользователя"
    )
    change_password_parser.add_argument(
        "--password_confirm", type=str, help="Подтвержнение пароля"
    )
    change_password_parser.set_defaults(func=change_password)

    args = parser.parse_args(sys.argv[1:])
    args.func(args)


if __name__ == "__main__":
    main()
