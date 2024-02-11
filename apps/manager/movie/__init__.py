from flask import Blueprint, render_template, request, redirect, url_for

from db.models import Movie, Hall, Screening, Coupon, MovieGenre, Genre

manager_movie_bp = Blueprint('manager_movie', __name__)


@manager_movie_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        original_language = request.form['original_language']
        overview = request.form['overview']
        poster_path = request.form['poster_path']
        release_date = request.form['release_date']
        duration_min = request.form['duration_min']
        Movie.create(
            title=title,
            original_language=original_language,
            overview=overview,
            poster_path=poster_path,
            release_date=release_date,
            duration_min=duration_min
        )
        return redirect(url_for('manager_movie.index'))
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    movies = Movie.get_any(offset=(page - 1) * size, limit=size)
    count = Movie.count()
    pages = count // size if count % size == 0 else count // size + 1
    currentPage = page
    return render_template('manager/movie.html', movies=movies, currentPage=currentPage, pages=pages)


@manager_movie_bp.route('/update', methods=['POST'])
def update_movie():
    body = request.form.to_dict()
    id = body.get('id', None)
    if id is None:
        return redirect(url_for('manager_movie.index'))
    del body['id']
    Movie.update_by_id(id=id, **body)
    return redirect(url_for('manager_movie.detail', mid=id))


@manager_movie_bp.route('/screening', methods=['POST'])
def screening():
    movie_id = request.form.get('movie_id', None)
    hall_id = request.form.get('hall_id', None)
    start_date_time = request.form.get('start_date_time', None)
    end_date_time = request.form.get('end_date_time', None)
    adult_price = request.form.get('adult_price', None)
    child_price = request.form.get('child_price', None)
    student_price = request.form.get('student_price', None)
    senior_price = request.form.get('senior_price', None)
    screen = Screening.create(
        movie_id=movie_id,
        hall_id=hall_id,
        start_date_time=start_date_time,
        end_date_time=end_date_time,
        available_seats=0,
        adult_price=adult_price,
        child_price=child_price,
        student_price=student_price,
        senior_price=senior_price
    )

    return redirect(url_for('manager_movie.detail', mid=movie_id))


@manager_movie_bp.route('/detail/<int:mid>')
def detail(mid):
    movie = Movie.get_by_id(id=mid)
    hall = Hall.get_any(limit=999)
    return render_template('manager/movie_detail.html', movie=movie, form=movie, hall=hall)


@manager_movie_bp.route('/delete/<int:sid>')
def screen_delete(sid):
    screen = Screening.get_by_id(id=sid)
    mid = screen.movie_id
    Screening.delete_by_id(id=sid)
    return redirect(url_for('manager_movie.detail', mid=mid))


@manager_movie_bp.route('/update_genre/<int:mid>',methods=['POST'])
def update_genre(mid):
    movie = Movie.get_by_id(id=mid)
    genre = request.json.get('genre')
    m_genres = MovieGenre.get_any(limit=9999,where=f"movie_id = {mid}")
    for i in m_genres:
        MovieGenre.delete_by_id(i.id)
    for i in genre:
        g = Genre.get_one(where=f"name = '{i}'")
        if g is None:
            g = Genre.create(name=i)
        MovieGenre.create(movie_id=movie.id, genre_id=g.id)

    return {}
