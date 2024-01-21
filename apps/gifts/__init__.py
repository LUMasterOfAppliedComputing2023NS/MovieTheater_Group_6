from flask import Blueprint, render_template

gifts_bp = Blueprint('gifts', __name__)

@gifts_bp.route('/')
def index():
    return render_template('gifts.html', show_search=True)

