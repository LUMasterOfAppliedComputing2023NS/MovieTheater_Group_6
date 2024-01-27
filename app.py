import datetime
import json

from flask import Flask, globals, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash

import config
from apps import auth
from apps.admin import admin_bp
from apps.bookings import bookings_bp
from apps.checkTicket import checkTicket_bp
from apps.contractUs import contractUs_bp
from apps.gifts import gifts_bp
from apps.home import home_bp
from apps.manager.movie import manager_movie_bp
from apps.manager.promotion import manager_promotion_bp
from apps.manager.report import manager_report_bp
from apps.manager.staff import manager_staff_bp
from apps.movies import movies_bp
from apps.moviesSchedule import moviesSchedule_bp
from apps.profile import profile_bp
from apps.promotions import promotions_bp
from db.models import User

app = Flask(__name__)
app.config.from_object(config)
auth.init_app(app)
app.register_blueprint(home_bp, url_prefix='/home')
app.register_blueprint(promotions_bp, url_prefix='/promotions')
app.register_blueprint(movies_bp, url_prefix='/movies')
app.register_blueprint(gifts_bp, url_prefix='/gifts')
app.register_blueprint(contractUs_bp, url_prefix='/contractUs')
app.register_blueprint(bookings_bp, url_prefix='/bookings')
app.register_blueprint(profile_bp, url_prefix='/profile')
app.register_blueprint(checkTicket_bp, url_prefix='/checkTicket')
app.register_blueprint(moviesSchedule_bp, url_prefix='/moviesSchedule')
app.register_blueprint(manager_movie_bp, url_prefix='/managerMovies')
app.register_blueprint(manager_staff_bp, url_prefix='/managerStaff')
app.register_blueprint(manager_promotion_bp, url_prefix='/managerPromotion')
app.register_blueprint(manager_report_bp, url_prefix='/managerReport')
app.register_blueprint(admin_bp, url_prefix='/admin')


# Homepage
@app.route('/')
def home():
    return redirect(url_for('home.index'))


@app.context_processor
def inject_globals():
    return dict(req=request, datetime=datetime.datetime, json=json)


with app.app_context():
    start_time = '10:00'
    end_time = '22.00'
    phone = '00000000'
    address = 'aaa bbb ccc'

    globals.g.setdefault('start_time', start_time)
    globals.g.setdefault('end_time', end_time)
    globals.g.setdefault('phone', phone)
    globals.g.setdefault('address', address)


@app.route('/g', methods=['GET'])
def g():
    if User.get_any(where="email = 'admin@test.com'").__len__() == 0:
        User.create(
            first_name='test',
            last_name='admin',
            email='admin@test.com',
            pass_hash=generate_password_hash('admin_pass'),
            is_admin=True,
            phone_number='12334567'
        )
    if User.get_any(where="email = 'staff@test.com'").__len__() == 0:
        User.create(
            first_name='test',
            last_name='staff',
            email='staff@test.com',
            pass_hash=generate_password_hash('staff_pass'),
            is_staff=True,
            phone_number='1233456'
        )
    if User.get_any(where="email = 'manager@test.com'").__len__() == 0:
        User.create(
            first_name='test',
            last_name='manager',
            email='manager@test.com',
            pass_hash=generate_password_hash('staff_pass'),
            is_manager=True,
            phone_number='123345678'
        )
    # user = User.get_one(where="email = 'admin@test.com'")
    # if user is not None:
    #     user.update_by_id(id=user.id, is_admin=True)
    # user = User.get_one(where="email = 'staff@test.com'")
    # if user is not None:
    #     user.update_by_id(id=user.id, is_staff=True)
    # user = User.get_one(where="email = 'manager@test.com'")
    # if user is not None:
    #     user.update_by_id(id=user.id, is_manager=True)
    return {'status': 'ok'}


if __name__ == '__main__':
    app.run()
