from flask import Flask, request, Response
from views import register_views
from services import SessionsService
from middlewaries import register_middlewaries 


app = Flask(__name__)

app.config["DEBUG"] = True
app.config["SESSION_COOKIE"] = "session_token"

register_views(app)
register_middlewaries(app)


if __name__ == "__main__":
    app.run("localhost", 9999)
