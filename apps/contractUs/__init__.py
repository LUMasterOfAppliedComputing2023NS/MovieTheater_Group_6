from flask import Blueprint, render_template

contractUs_bp = Blueprint('contractUs', __name__)

@contractUs_bp.route('/')
def index():
    return render_template('contractUs.html', show_search=True)

