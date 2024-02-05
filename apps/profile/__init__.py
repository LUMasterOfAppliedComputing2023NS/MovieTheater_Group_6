from flask import Blueprint, render_template, request, flash
from flask_login import current_user, AnonymousUserMixin, login_user
from werkzeug.security import generate_password_hash

from db.models import Coupon, User

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        phone_number = request.form['phone_number']
        address = request.form['address']
        date_of_birth = request.form['date_of_birth']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        if email and phone_number and address and date_of_birth and first_name and last_name:
            User.update_by_id(id=current_user.id,email=email,phone_number=phone_number,address=address,date_of_birth=date_of_birth,last_name=last_name,first_name=first_name)
        else:
            flash('param required')
    return render_template('profile.html')


@profile_bp.route('/change_password', methods=['POST'])
def change_password():
    newPassword = request.form['newPassword']
    confirmNewPassword = request.form['confirmNewPassword']
    if newPassword != confirmNewPassword:
        flash('Two passwords do not match')
    else:
        User.update_by_id(id=current_user.id, pass_hash=generate_password_hash(newPassword))
    return render_template('profile.html')