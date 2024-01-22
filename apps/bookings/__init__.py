import json

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user

from db.models import Coupon, Booking, Seat, Payment, User

bookings_bp = Blueprint('bookings', __name__)


@bookings_bp.route('/', methods=['GET', 'POST'])
def index():
    bookings = Booking.get_any(limit=999,where="user_id={}".format(current_user.id))
    return render_template('bookings.html',bookings=bookings)


@bookings_bp.route('/pay', methods=['GET', 'POST'])
def pay():
    seats = request.args.get('seats', '[]')
    sid = request.args.get('sid', None)
    movie_id = request.args.get('movie_id', None)
    adult = request.args.get('adult', 0)
    child = request.args.get('child',0)
    student = request.args.get('student', 0)
    senior = request.args.get('senior', 0)
    price_total = float(request.args.get('price_total', 0))
    m = 'gift card'
    if float(current_user.gift_card) < float(price_total):
        User.update_by_id(id=current_user.id, gift_card=0)
        m = 'gift card and online bank merge'
        if float(current_user.gift_card) == 0:
            m = 'online bank'
    else:
        User.update_by_id(id=current_user.id, gift_card=float(current_user.gift_card) - float(price_total))
    seats = json.loads(seats)
    coupon_id = request.args.get('coupon_id', None)
    c = Coupon.get_by_id(coupon_id)
    coupon = Coupon.update_by_id(id=coupon_id, used_counter=c.used_counter+len(seats))
    booking = Booking.create(user_id=current_user.id,screening_id=sid, seats=seats,price_total=price_total)
    payment = Payment.create(user_id=current_user.id,booking_id=booking.id,payment_method=m,coupon_id=coupon.id,amount=price_total,final_amount=price_total)
    Booking.update_by_id(id=booking.id, payment_id=payment.id)
    return redirect(url_for('bookings.index'))


@bookings_bp.route('/cancel/<int:bid>')
def cancel(bid):
    booking = Booking.get_by_id(bid)
    coupon = Coupon.get_by_id(booking.payment.coupon_id)
    Coupon.update_by_id(coupon.id,used_counter=coupon.used_counter-1)
    Payment.delete_by_id(booking.payment_id)
    Booking.delete_by_id(id=bid)
    return redirect(url_for('bookings.index'))
