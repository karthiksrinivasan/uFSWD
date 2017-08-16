from app import server
from flask import Blueprint
from flask_oauthlib.client import OAuth


users = Blueprint('users', __name__,
                  template_folder='templates')

# Instantiating Google Authentication Module
oauth = OAuth(server)
google = oauth.remote_app(
    'google',
    consumer_key=server.config['GOOGLE_ID'],
    consumer_secret=server.config['GOOGLE_SECRET'],
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

from app.modules.users import views
