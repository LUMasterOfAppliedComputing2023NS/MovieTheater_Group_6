import os.path
from datetime import date

import bcrypt
import flask_login
from flask import Flask, request, url_for, flash
from flask import redirect
from flask import render_template
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, logout_user

from controller import Controller
from database.db_credential import DbCredential
from forms import LoginForm, RegisterForm
from model.user import User
from app_constants import TmdbConstants

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

db_credential: DbCredential
if os.path.exists('db_connection.py'):
    from db_connection import db_credential as pa_credential
    db_credential = pa_credential
else:
    raise Exception(
        "unable to find db_connection.py, please refer to db_connection.py.example and create one with correct db connection credentials")

controller = Controller(db_credential)
salt = bcrypt.gensalt()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # type: ignore


@login_manager.unauthorized_handler
def handle_needs_login():
    flash("You have to be logged in to access this page.")
    return redirect(url_for('login', next=request.endpoint))


@app.route("/poster/<poster_path>", methods=["GET"])
def poster_url(poster_path: str):
    return redirect(f"{TmdbConstants.tmdb_poster_api_url}{poster_path}")

@login_manager.user_loader
def load_user(user_id: str):
    try:
        return controller.get_user_by_id(user_id)
    except:
        print(f"unable to get user for id:{user_id}, unable to parse as int")
        return None


@app.route('/reset_db')
def reset_db():
    logout_user()
    controller.reset_db(recreate_db=True, load_preset_data=True, load_tmdb_movie=True)
    return "db reset done"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Get Form Fields
    login_form = LoginForm(request.form)

    if request.method == 'POST':
        # When user clicked on submit from login page
        if login_form.login_submit.data and login_form.validate_on_submit():

            email = login_form.email_address.data
            password = login_form.password.data
            remember_me = login_form.remember_me.data

            if email is None or len(email) == 0:
                login_form.email_address.errors.append("Email is empty")
                return render_template('login/login.html', login_form=login_form, register_link=url_for('register'))

            # Get user by email
            user = controller.get_user({'email': email}) or "unable to find user with given credentials"

            if user and isinstance(user, User) \
                    and password \
                    and isinstance(password, str) \
                    and bcrypt.checkpw(password.encode('utf-8'), user.pass_hash.encode('utf-8')):
                flask_login.login_user(user, remember=remember_me)
                return redirect(url_for('home'))
            elif isinstance(user, str):
                login_form.email_address.errors.append(str)
            else:
                login_form.email_address.errors.append("Invalid user credentials, please check again")

    return render_template('login/login.html', login_form=login_form, register_link=url_for('register'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST':
        # When user clicked on submit from register page
        if form.is_submitted():
            error_out = False
            email = form.email_address.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            phone_number = form.phone_number.data
            address = form.address.data
            password = form.password.data.encode('utf-8')
            confirm_password = form.confirm_password.data.encode('utf-8')

            if form.validate():
                pass

            if password != confirm_password:
                form.password.errors.append("Password does not match")
                error_out = True

            if email is not None and len(email) != 0:
                user = controller.get_user({'email': email})
                if user is not None:
                    form.email_address.errors.append("Email already in use")
                    error_out = True

            # display error if needed
            if error_out:
                return render_template('login/register.html', form=form)

            # create user
            pass_hash = bcrypt.hashpw(password, salt)
            user_dict = {
                'first_name': first_name,
                'last_name': last_name,
                'address': address,
                'email': email,
                'pass_hash': pass_hash,
                'phone_number': phone_number,
                'date_joined': date.today(),
                'is_staff': 0,
                'is_admin': 0,
                'is_manager': 0,
            }

            user = controller.create_user(user_dict)
            flash("You are now registered, logging in...", 'success')
            flask_login.login_user(user, remember=True)
            return redirect(url_for('home'))

    return render_template('login/register.html', form=form)


# Homepage
@app.route('/')
def home():
    showing_movies = controller.get_showing_movies()
    up_coming_movies = controller.get_upcoming_movies()
    return render_template('home.html', showing_movies=showing_movies, up_coming_movies=up_coming_movies)




if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)