import json
from flask import abort, redirect, render_template, request, url_for, flash
from utils import get_password_hash

from services import SessionsService, UsersService
from .schemas import user_credentials_schema


def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not user_credentials_schema.validate(request.form):
            abort(400)
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
        if not user_credentials_schema.validate(request.form):
            flash(f"Invalid data; Errors: {json.dumps(user_credentials_schema.errors)}")
            return redirect(url_for("auth.register"))
        user = UsersService.create_user(username, password)
        SessionsService.attach_user(request.session_token, user.id)
        return redirect(url_for("index_page"))


def logout():
    res = redirect("/")
    SessionsService.delete_session_by_token(request.session_token)
    res.set_cookie("session_token", "")
    return res
