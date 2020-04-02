from flask import abort, redirect, render_template, request, url_for
from utils import get_password_hash

from services import SessionsService, UsersService


def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password = get_password_hash(password)
        user = UsersService.get_user_by_username(username)
        if user.password != password:
            abort(400)
        SessionsService.attach_user(request.session_token, user.id)
        return redirect(url_for("index_page"))


def register():
    if request.method == "GET":
        return render_template("registration.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = UsersService.create_user(username, password)
        SessionsService.attach_user(request.session_token, user.id)
        return redirect(url_for("index_page"))


def logout():
    res = redirect("/")
    SessionsService.delete_session_by_token(request.session_token)
    res.set_cookie("session_token", "")
    return res
