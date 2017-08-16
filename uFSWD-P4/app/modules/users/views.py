from app.modules.users import users, google
from flask import render_template, abort, redirect, request, url_for, session
from flask_login import current_user, login_user, logout_user, UserMixin
from app import server, login_manager


class User(UserMixin):
    """ User Object for working with Login Manager"""

    def __init__(self, resp):
        """ Storing the response from Google authentication as User object"""
        self.id = resp["id"]
        self.email = resp["email"]
        self.given_name = resp["given_name"]
        self.name = resp["name"]
        self.picture = resp["picture"]
        self.link = resp.get("link", "")


@users.route('/login')
def login():
    # If the user had already logged in - redirect to index page
    if not current_user.is_anonymous:
        return redirect(url_for('index.index_page'))
    # Otherwise authorize using google
    return google.authorize(callback=url_for('users.authorized',
                                             _external=True))


@users.route('/logout')
def logout():
    # Logout the user by removing the google_token from session cookie
    if 'google_token' in session:
        session.pop('google_token', None)
        logout_user()
    return redirect(url_for('index.index_page'))


@users.route('/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    login_user(User(me.data), remember=True)
    return redirect(url_for('index.index_page'))


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


@login_manager.user_loader
def load_user(user_id):
    # Load User object based on session token
    if 'google_token' in session:
        me = google.get('userinfo')
        try:
            user = User(me.data)
        except KeyError:
            # If the session token is expired then logout the user
            session.pop('google_token', None)
            logout_user()
            return None
        return user
    else:
        return None
