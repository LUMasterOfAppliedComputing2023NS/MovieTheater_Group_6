import datetime
import json

from flask import Blueprint, render_template, request, redirect, flash, url_for

from db.models import Movie, Screening, Seat, Booking, Coupon

movies_bp = Blueprint('movies', __name__)


@movies_bp.route('/')
def index():
    movies = Movie.get_any(limit=9999,
                           where="id in (select movie_id from screening where TIME(start_date_time) > TIME(NOW()) and DATE(start_date_time) = DATE(NOW()))")
    soon = Movie.get_any(limit=9999,
                         where="id in (select movie_id from screening where TIMESTAMP(start_date_time) > TIMESTAMP(NOW()) and DATE(start_date_time) > DATE(NOW()))")
    return render_template('movies.html', movies=movies, soon=soon)


@movies_bp.route('detail/<int:movie_id>')
def detail(movie_id):
    movie = Movie.get_by_id(movie_id)
    date = request.args.get('date', None)
    time = request.args.get('time', None)
    sid = request.args.get('sid', None)
    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    screening = None
    seats = None
    select_screening = None
    hall = None
    if date is not None:
        screening = Screening.get_any(limit=9999,
                                      where=f"movie_id = {movie.id} and DATE(start_date_time) = DATE('{date}')")
        if time is not None:
            if sid is not None:
                select_screening = Screening.get_by_id(sid)
            else:
                select_screening = Screening.get_one(where=f"movie_id = {movie.id} and DATE(start_date_time) = DATE('{date}') and TIME(start_date_time) > TIME('{time}')")
            hall = select_screening.get_hall
            bookings = Booking.get_any(limit=9999, where=f"screening_id = {select_screening.id}")
            seats = []
            for i in bookings:
                seats += [str(j) for j in json.loads(i.seats)]
    return render_template('movie_detail.html',sid=sid, movie=movie, date=date, time=time, screening=screening, seats=seats,booking_seats=seats,hall=hall,select_screening=select_screening)


@movies_bp.route('proceed/<int:movie_id>')
def proceed(movie_id):
    seats = json.loads(request.args.get('seats', '[]'))
    sid = request.args.get('sid', None)
    if sid is None:
        flash('No screening found')
        return redirect(url_for('movies.detail', movie_id=movie_id))
    select_screening = Screening.get_by_id(sid)
    movie = Movie.get_one(movie_id)
    """ col-row """
    seats = [i.split('-') for i in seats]
    coupons = Coupon.get_any(limit=999, where=f"expiry_date > now()")
    return render_template('movie_proceed.html',seats=seats,movie=movie,select_screening=select_screening,coupons=coupons)
