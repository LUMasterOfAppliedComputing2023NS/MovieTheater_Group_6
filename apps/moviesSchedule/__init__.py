from flask import Blueprint, render_template

from db.models import Movie

moviesSchedule_bp = Blueprint('moviesSchedule', __name__)


@moviesSchedule_bp.route('/')
def index():
    movies = Movie.get_any(limit=9999,
                           where="id in (select movie_id from screening where TIMESTAMP(start_date_time) > TIMESTAMP(NOW()) and DATE(start_date_time) = DATE(NOW()))")
    soon = Movie.get_any(limit=9999,
                         where="id in (select movie_id from screening where TIMESTAMP(start_date_time) > TIMESTAMP(NOW()) and DATE(start_date_time) > DATE(NOW()))")

    return render_template('moviesSchedule.html', movies=movies, soon=soon)
