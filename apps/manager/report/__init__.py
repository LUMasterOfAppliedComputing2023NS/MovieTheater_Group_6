import datetime

from flask import Blueprint, render_template, request

from db import get_session
from db.models import Booking, GiftCardLog, Movie

manager_report_bp = Blueprint('manager_report', __name__)

def get_dates_between_dates(start_date, end_date):
    current_date = start_date
    dates = []
    while current_date <= end_date:
        dates.append(current_date.strftime("%Y-%m-%d"))
        current_date += datetime.timedelta(days=1)
    return dates

@manager_report_bp.route('/')
def index():
    start_date = request.args.get('start_date', None)
    end_date = request.args.get('end_date', datetime.date.today().strftime('%Y-%m-%d'))
    movie_id = request.args.get('movie_id', None)

    print(start_date, end_date)

    where = []
    card_where = []
    if start_date:
        where.append(" DATE(created_date_time) >= DATE('" + start_date + "') ")
        card_where.append(" DATE(create_at) >= DATE('" + start_date + "') ")
    if end_date:
        where.append(" DATE(created_date_time) <= DATE('" + end_date + "') ")
        card_where.append(" DATE(create_at) <= DATE('" + end_date + "') ")
    if movie_id:
        movie_id = int(movie_id)
        where.append(f" screening_id in (select id from screening where movie_id = {movie_id}) ")
    where_str = 'and'.join(where)
    card_str = 'and'.join(card_where)
    total_gift_card = GiftCardLog.get_total_money(where=card_str if card_str else '0=0')
    total_order = Booking.count(where=where_str if where_str else '0=0')
    total_tickets = Booking.get_ticket(where=where_str if where_str else '0=0')
    s, conn = get_session()


    if not start_date:
        res = s.execute(f"""
            select DATE(created_date_time) from booking order by created_date_time desc limit 1
        """)
        ticket_start_date = s.fetchone()[0]
        res = s.execute(f"""
            select DATE(create_at) from gift_card_log order by create_at desc limit 1
        """)
        card_start_date = s.fetchone()[0]
    else:
        ticket_start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        card_start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    ticket_dates = get_dates_between_dates(ticket_start_date, end_date)
    card_dates = get_dates_between_dates(card_start_date, end_date)
    res = s.execute(f"""
            select sum(price_total),DATE(created_date_time) from booking where {where_str if where_str else '0=0'} group by DATE(created_date_time)
        """)
    t = {i[1].strftime('%Y-%m-%d'): float(i[0]) for i in s.fetchall()}
    print(t)
    ticket_chart = [t.get(i,0) for i in ticket_dates]
    res = s.execute(f"""
        select sum(point),DATE(create_at) from gift_card_log where {card_str if card_str else '0=0'} group by DATE(create_at)
    """)
    t = {i[1].strftime('%Y-%m-%d'):int(i[0]) for i in s.fetchall()}
    print(t)
    card_chart = [t.get(i,0) for i in card_dates]

    movies = Movie.get_any()

    return render_template('manager/report.html', total_gift_card=total_gift_card
                           , total_order=total_order, total_tickets=total_tickets,
                           ticket_dates=ticket_dates, card_dates=card_dates, card_chart=card_chart,
                           ticket_chart=ticket_chart,movie_id=movie_id,movies=movies,start_date=start_date,end_date=end_date)
