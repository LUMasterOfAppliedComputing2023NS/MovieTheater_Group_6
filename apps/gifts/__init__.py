from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user

from db.models import User, GiftCardLog

gifts_bp = Blueprint('gifts', __name__)


@gifts_bp.route('/')
def index():
    return render_template('gifts.html')


@gifts_bp.route('/pay', methods=['POST'])
def pay():
    gift = request.form.get('gift')
    User.update_by_id(id=current_user.id, gift_card=float(current_user.gift_card) + int(gift))
    GiftCardLog.create(point=int(gift), user_id=current_user.id)
    return redirect(url_for('gifts.index'))
