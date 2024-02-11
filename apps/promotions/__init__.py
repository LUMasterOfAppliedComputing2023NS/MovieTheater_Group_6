from flask import Blueprint, render_template

from db.models import Coupon

promotions_bp = Blueprint('promotions', __name__)


@promotions_bp.route('/')
def index():
    coupon = Coupon.get_any(limit=999, where=f'is_active = 1')
    return render_template('promotions.html', coupon=coupon)
