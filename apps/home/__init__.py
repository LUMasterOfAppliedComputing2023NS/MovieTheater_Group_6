import datetime

from flask import Blueprint, render_template, request

from db.models import Movie, Screening

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def index():
    now_showing_limit = request.args.get('now_showing_page_size', 4, int)
    now_showing_page_num = request.args.get('now_showing_page_num', 1, int)
    now_showing_offset = (now_showing_page_num - 1) * now_showing_limit
    today = datetime.date.today()
    now_showing_where = f"TIME(start_date_time) > TIME(NOW()) and DATE(start_date_time) = DATE(NOW())"
    now_showing: list[Screening] = Screening.get_any(
        limit=now_showing_limit,
        offset=now_showing_offset,
        where=now_showing_where
    )
    now_showing_count = Screening.count(where=now_showing_where)
    coming_soon_limit = request.args.get('coming_soon_page_size', 2, int)
    coming_soon_page_num = request.args.get('coming_soon_page_num', 1, int)
    coming_soon_offset = (coming_soon_page_num - 1) * coming_soon_limit
    coming_soon_where = f"Date(start_date_time) > {today.strftime('%Y-%m-%d')}"
    coming_soon_screening: list[Screening] = Screening.get_any(
        limit=99999,
        where=coming_soon_where
    )
    c_ids = set([str(i.movie_id) for i in coming_soon_screening])
    print(c_ids)
    coming_soon = Movie.get_any(limit=coming_soon_limit, offset=coming_soon_offset, where=f" id in ({','.join(c_ids)})")
    coming_soon_count = Screening.count(where=coming_soon_where)
    return render_template('home.html',
                           show_search=True,
                           now_showing=now_showing,
                           coming_soon=coming_soon,
                           now_showing_next_page=now_showing_page_num + 1,
                           coming_sonn_next_page=coming_soon_page_num + 1,
                           now_showing_page=now_showing_page_num,
                           coming_soon_page=coming_soon_page_num,
                           now_showing_pre_page=now_showing_page_num - 1 if now_showing_page_num > 1 else None,
                           coming_sonn_pre_page=coming_soon_page_num - 1 if coming_soon_page_num > 1 else None,
                           now_showing_count=now_showing_count,
                           coming_soon_count=coming_soon_count
                           )
