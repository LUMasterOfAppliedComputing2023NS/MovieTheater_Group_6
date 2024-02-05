from datetime import date
from io import BytesIO
from captcha.image import ImageCaptcha
import random, string
import flask_login
from flask import Blueprint, redirect, url_for, request, flash, Flask, render_template, make_response, session
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

@auth_bp.route('/verify-code/')
def verify_code():
    captcha = random.choices('0123456789',k=4)
    img = ImageCaptcha()
    image = img.generate_image(chars=captcha)
    session['code'] = ''.join(captcha)
    # with open('captcha.png','wb') as fp:
    #     image.save(fp,"png")
    out = BytesIO()
    image.save(out, 'png')
    # 把out的文件指针指向最开始的位置
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp


# Login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Get Form Fields
    login_form = LoginForm(request.form)
    register_form = RegisterForm(request.form)

    if request.method == 'POST':
        v_code = request.form['code']
        print(v_code,session.get('code',"<>"))
        if v_code != session.get('code',"<>"):
            flash('verification code incorrect')
            return render_template('login/login.html', login_form=login_form, form=register_form)

        # When user clicked on submit from login page
        if login_form.login_submit.data and login_form.validate_on_submit():

            email = login_form.email_address.data
            password = login_form.password.data
            remember_me = login_form.remember_me.data

            if email is None or len(email) == 0:
                flash("Email is empty")
                return render_template('login/login.html', login_form=login_form, form=register_form)

            # Get user by email
            user = User.get_one(where=f'`email`="{email}"') or "unable to find user with given credentials"
            if user and isinstance(user, User) \
                    and password \
                    and isinstance(password, str) \
                    and check_password_hash(pwhash=user.pass_hash, password=password):
                flask_login.login_user(user, remember=remember_me)
                return redirect(url_for('home'))
            elif isinstance(user, str):
                flash(user)
            else:
                flash("password error")
    return render_template('login/login.html', login_form=login_form, form=register_form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    login_form = LoginForm()
    if request.method == 'POST':
        v_code = request.form['code']
        if v_code != session.get('code',"<>"):
            flash('verification code incorrect')
            return render_template('login/login.html', login_form=login_form,form=form)

        # When user clicked on submit from register page
        if form.is_submitted():
            error_out = False
            email = form.email_address.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            phone_number = form.phone_number.data
            address = form.address.data
            password = form.password.data
            confirm_password = form.confirm_password.data

            if form.validate():
                pass

            if password != confirm_password:
                flash("Password does not match")
                error_out = True

            if email is not None and len(email) != 0:
                user = User.get_one(f'`email`="{email}"')
                if user is not None:
                    flash("Email already in use")

            # display error if needed
            if error_out:
                return render_template('login/login.html',login_form=login_form, form=form)

            # create user

            pass_hash = generate_password_hash(password)
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
        except Exception as e:
            print(e)
            print(f"unable to get user for id:{user_id}, unable to parse as int")
            return None

    @app.before_request
    def before_request():
        pass

    app.register_blueprint(auth_bp, url_prefix='/auth')
