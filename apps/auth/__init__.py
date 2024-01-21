from datetime import date
import flask_login
from flask import Blueprint, redirect, url_for, request, flash, Flask, render_template
from flask_login import LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from apps.auth.forms import LoginForm, RegisterForm
from db.models import User

auth_bp = Blueprint('auth', __name__)
login_manager = LoginManager()


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# Login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Get Form Fields
    login_form = LoginForm(request.form)
    register_form = RegisterForm(request.form)

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
            user = User.get_one(f'`email`="{email}"') or "unable to find user with given credentials"
            if user and isinstance(user, User) \
                    and password \
                    and isinstance(password, str) \
                    and check_password_hash(pwhash=user.pass_hash, password=password):
                flask_login.login_user(user, remember=remember_me)
                return redirect(url_for('home'))
            elif isinstance(user, str):
                login_form.email_address.errors.append(user)
            else:
                login_form.email_address.errors.append("Invalid user credentials, please check again")
    return render_template('login/login.html', login_form=login_form, form=register_form)


@auth_bp.route('/register', methods=['GET', 'POST'])
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
                user = User.get_one(f'`email`="{email}"')
                if user is not None:
                    form.email_address.errors.append("Email already in use")
                    error_out = True

            # display error if needed
            if error_out:
                return render_template('login/register.html', form=form)

            # create user
            pass_hash = generate_password_hash(password.decode('utf-8'))
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

            user = User.create(**user_dict)
            flash("You are now registered, logging in...", 'success')
            flask_login.login_user(user, remember=True)
            return redirect(url_for('home'))

    return redirect('auth.login')


def init_app(app: Flask):
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # type: ignore

    @login_manager.unauthorized_handler
    def handle_needs_login():
        flash("You have to be logged in to access this page.")
        return redirect(url_for('login', next=request.endpoint))

    @login_manager.user_loader
    def load_user(user_id: str):
        try:
            return User.get_by_id(user_id)
        except:
            print(f"unable to get user for id:{user_id}, unable to parse as int")
            return None

    @app.before_request
    def before_request():
        pass

    app.register_blueprint(auth_bp, url_prefix='/auth')
