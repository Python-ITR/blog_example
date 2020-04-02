from os import path
from flask import Blueprint
from .views import login, logout, register

CURRENT_DIR = path.dirname(path.abspath(__file__))
TEMPLATES_FOLDER = path.join(CURRENT_DIR, "templates")

auth_blueprint = Blueprint("auth", __name__, template_folder=TEMPLATES_FOLDER)

auth_blueprint.route("/login", methods=["GET", "POST"])(login)
auth_blueprint.route("/registration", methods=["GET", "POST"])(register)
auth_blueprint.route("/logout")(logout)