import json

from flask import Blueprint, render_template, request, redirect, url_for

from db.models import Coupon, Screening, Booking

checkTicket_bp = Blueprint('checkTicket', __name__)


@checkTicket_bp.route('/')
def index():
    screenings = Screening.get_any(limit=999,
                                   order_by="start_date_time",
                                   where=f"Date(start_date_time) = DATE(now()) and TIME(start_date_time) > TIME(now())")
    select_screening = None
    seats = None
    hall = None
    select_screening_id = request.args.get('sid', None)
    bookings = []
    ticket_seats = []
    if select_screening_id is not None:
        select_screening = Screening.get_by_id(select_screening_id)
        bookings = Booking.get_any(limit=9999,order_by='status', where=f"screening_id = {select_screening.id}")
        seats = []
        ticket_seats = []
        hall = select_screening.get_hall
        for i in bookings:
            seats += [str(j) for j in json.loads(i.seats)]
            if i.status == 1:
                ticket_seats += [str(j) for j in json.loads(i.seats)]
    return render_template('checkTicket.html',
                           hall=hall,
                           screenings=screenings,
                           seats=seats,
                           booking_seats=seats,
                           select_screening=select_screening,
                           ticket_seats=ticket_seats,
                           bookings=bookings)

@checkTicket_bp.route('/checkTicket/<int:bid>')
def ticket(bid):
    Booking.update_by_id(bid, status=1)
    return redirect(url_for('checkTicket.index'))
