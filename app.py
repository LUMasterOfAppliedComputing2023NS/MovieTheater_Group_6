# from flask_bcrypt import Bcrypt
import os.path

import bcrypt
from flask import Flask
from flask import redirect
from flask import render_template
from flask_login import LoginManager

from database.database import Database
from database.db_credential import DbCredential

#
# import app_constants
# import database
# from form import ChangePasswordForm, ProfileForm, RegisterForm, LoginForm, EditMovieForm, CreateOrEditStaffForm
# from model import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

db_credential: DbCredential
# use python anywhere credential when file exists
if os.path.exists('pa_connection.py'):
    from pa_connection import db_credential as pa_credential

    db_credential = pa_credential
else:
    from local_connection import db_credential as local_credential

    db_credential = local_credential

db = Database(db_credential)

# bcrypt: Bcrypt = Bcrypt(app)
salt = bcrypt.gensalt()

login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view = 'login'  # type: ignore

@login_manager.user_loader
def load_user(user_id: str):
    try:
        return db.get_user(int(user_id))
    except:
        print(f"unable to get user for id:{user_id}, unable to parse as int")
        return None



# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login/login.html')


# Homepage
@app.route('/')
def home():
    return redirect('login')

#
# # handles login and registration
# @app.route('/login', methods=['GET', 'POST'])  # type: ignore
# def login():
#     if current_user is not None \
#             and isinstance(current_user, User) \
#             and current_user.is_authenticated:
#         flask_login.login_user(current_user)
#         return redirect(url_for('home'))
#
#     login_form = LoginForm()
#     register_form = RegisterForm()
#
#     def success_login(user: User, remember: bool = False) -> Response:
#         session['loggedin'] = True
#         session['id'] = user.id
#         session['name'] = user.name
#         flask_login.login_user(user, remember=remember)
#         print(f"login success: {user}")
#         return redirect(url_for('home'))
#
#     print(f"login_form.errors:{login_form.errors} register_form.errors:{register_form.errors}")
#     _from = request.args.get('from', None, type=str)
#
#     # and login_form.LoginSubmit.data
#     if _from == 'login' and login_form.validate_on_submit():
#         email = login_form.EmailAddress.data
#         user = db.load_user_by_email(email) if email is not None and len(
#             email) != 0 else "Empty email"
#         password = login_form.Password.data
#         error: str | None = None
#
#         if user and isinstance(user, User) and password and isinstance(password, str):
#
#             if bcrypt.checkpw(
#                     password.encode('utf-8'), user.pass_hash.encode('utf-8')
#             ):
#                 return success_login(user)
#
#         error = "Invalid user credentials, please check again"
#         print(error)
#         flash(error)
#     # register_form.RegisterSubmit.data
#     elif _from == 'register' and register_form.validate_on_submit():
#         email = register_form.EmailAddress.data
#         password = register_form.Password.data.encode('utf-8')
#         user_type = register_form.UserType.data
#
#         # check if email in use
#         if email is None or len(email) == 0:
#             flash("invalid input")
#             return
#
#         existing_user = db.load_user_by_email(email)
#         if isinstance(existing_user, User):
#             flash("email already in use")
#             return redirect(url_for('login'))
#
#         pass_hash = bcrypt.hashpw(password, salt)
#         user_dict = {
#             'name': register_form.FullName.data,
#             'phone_number': register_form.PhoneNumber.data,
#             'email': email,
#             'pass_hash': pass_hash,
#             'address': register_form.Address.data,
#             'date_joined': date.today()
#         }
#
#         if user_type == 'staff':
#             user_dict['is_staff'] = 1
#         elif user_type == 'admin':
#             user_dict['is_admin'] = 1
#
#         new_user = db.create_user(user_dict)
#         return success_login(new_user)
#
#     return render_template(
#         "login.html",
#         login_form=login_form,
#         register_form=register_form
#     )
#
#
# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('home'))
#
#
# @app.route('/password', methods=['GET', 'POST'])
# @login_required
# def change_password():
#     form = ChangePasswordForm()
#     if form.submit.data and form.validate_on_submit():
#         if current_user and isinstance(current_user, User):
#             current_user_id = current_user.id
#             current_password = form.current_password.data.encode('utf-8')
#             new_password = form.new_password.data
#
#             if not new_password or len(new_password) == 0:
#                 flash("new password is empty")
#                 return redirect(url_for('change_password'))
#
#             if bcrypt.checkpw(current_password, current_user.pass_hash.encode('utf-8')):
#                 pass_hash = bcrypt.hashpw(new_password.encode('utf-8'), salt)  # type: ignore
#                 new_user = db.update_user_password(current_user_id, pass_hash)
#                 flash("new password saved")
#                 return redirect(url_for('home'))
#             else:
#                 flash("unable to validate old password")
#         else:
#             redirect(url_for('login'))
#
#         pass
#     return render_template("change_password.html", form=form)
