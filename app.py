from flask import Flask
from login_manager import login_manager
from controller import endpoints
import secrets

# Set up app
app = Flask(__name__)
app.register_blueprint(endpoints)

# Generate secret server key
app.secret_key = secrets.token_hex(16)

# Add a login manager to the app
login_manager.init_app(app)
login_manager.login_view = "endpoints.login"
