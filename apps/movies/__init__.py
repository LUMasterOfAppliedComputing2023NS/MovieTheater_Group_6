from flask import Blueprint, render_template

movies_bp = Blueprint('movies', __name__)

@movies_bp.route('/')
def index():
    return render_template('movies.html', show_search=True)

