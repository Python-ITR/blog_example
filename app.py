import os
import dotenv
from flask import Flask
from views import register_views
from middlewaries import register_middlewaries
from admin import admin_blueprint
from auth import auth_blueprint

dotenv.load_dotenv()

app = Flask(__name__)

app.config["DEBUG"] = os.environ.get("DEBUG", None) in ["1", "true", "True"]
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "")
app.config["SESSION_COOKIE"] = "session_token"

register_views(app)
register_middlewaries(app)

app.register_blueprint(admin_blueprint)
app.register_blueprint(auth_blueprint)


if __name__ == "__main__":
    app.run("localhost", 9999)
