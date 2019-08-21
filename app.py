# Imports

from flask          import Flask, g
from flask_cors     import CORS
from flask_login    import LoginManager
from api.user       import user
from api.parks      import park

import models


# ------------------------------------------------------------------------------------------------------

# Setup and Initialization

DEBUG           = True
PORT            = 9000
login_manager   = LoginManager()
app             = Flask(__name__, static_url_path="", static_folder="static")


# ------------------------------------------------------------------------------------------------------

# Session

app.secret_key  = 'RANDOM ASS STRING'
app.register_blueprint(user)
app.register_blueprint(park)


# CORS(api, origins = ['http://localhost:3000'], supports_credentials = True)
# CORS(user, origins = ['http://localhost:3000'], supports_credentials = True)


login_manager.init_app(app)


# ------------------------------------------------------------------------------------------------------

# Decorators and Functions

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    """Connect to the database before each request"""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the database connection after each request"""
    g.db.close()
    return response

@app.route('/')
def index():
    return 'hi'


# ------------------------------------------------------------------------------------------------------

# Run the App!

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
