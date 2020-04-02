from flask import Flask, request, Response
from views import register_views
from services import SessionsService
from middlewaries import register_middlewaries
from admin import admin_blueprint
from auth import auth_blueprint


app = Flask(__name__)

app.config["DEBUG"] = True
app.config["SESSION_COOKIE"] = "session_token"

register_views(app)
register_middlewaries(app)

app.register_blueprint(admin_blueprint)
app.register_blueprint(auth_blueprint)


if __name__ == "__main__":
    app.run("localhost", 9999)
