from flask import Blueprint, render_template, g

contractUs_bp = Blueprint('contractUs', __name__)

@contractUs_bp.route('/')
def index():
    start_time = g.get('start_time')
    end_time = g.get('end_time')
    address = g.get('address')
    phone = g.get('phone')
    return render_template('contractUs.html', show_search=True,start_time=start_time, end_time=end_time, phone=phone, address=address)

