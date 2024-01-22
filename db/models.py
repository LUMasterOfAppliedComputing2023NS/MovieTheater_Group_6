import json
from abc import ABCMeta
from datetime import date, datetime

from werkzeug.security import generate_password_hash

from . import get_session


def value_format(v):
    if isinstance(v, str):
        return f'"{v}"'
    if isinstance(v, date):
        return f'"{v.year}-{v.month}-{v.day}"'
    if isinstance(v, datetime):
        return f'"{v.year}-{v.month}-{v.day}T{v.hour}:{v.minute}:{v.second}"'
    if isinstance(v, float) or isinstance(v, int):
        return f'{v}'
    if isinstance(v, bool):
        return f'{1 if v else 0}'
    if isinstance(v, bytes):
        return f'"{v.decode("utf-8")}"'
    if v is None:
        return 'null'
    if isinstance(v, list):
        return f"json_array({','.join([value_format(i) for i in v])})"


def values_formatter(values):
    res = []
    for v in values:
        res.append(value_format(v))
    print(res)
    return ','.join(res)


class BaseModel(metaclass=ABCMeta):
    fields = []
    is_log = True
    table_name = ''

    def __init__(self, **kwargs):
        self.is_log = kwargs.get('is_log', True)

    @classmethod
    def format(cls, **keyword):
        return cls(**keyword)

    @classmethod
    def create(cls, **kwargs):
        s, conn = get_session()
        if kwargs.get('password',None) is not None:
            kwargs['pass_hash'] = generate_password_hash(kwargs.get('password', ''))
            del kwargs['password']
        try:
            sql = f"""
             insert into  `{cls.table_name}`(`{'`,`'.join(kwargs.keys())}`) values ({values_formatter(kwargs.values())});
           """
            if cls.is_log:
                print(sql)
            s.execute(sql)
            conn.commit()
            return cls.get_one()
        except Exception as e:
            conn.rollback()
            raise e

    @classmethod
    def get_any(cls,
                limit=10,
                offset=0,
                order_by='id desc',
                where='0=0'
                ):
        s, conn = get_session()
        try:
            sql = f"""
                select `{'`,`'.join(cls.fields)}` 
                from {cls.table_name} 
                where {where} 
                order by {order_by}
                limit {limit} 
                offset {offset};
               """
            if cls.is_log:
                print(sql)
            s.execute(sql)
            db_res = s.fetchall()
            res = []
            for i in db_res:
                res.append(cls.format(**{k: v for k, v in zip(cls.fields, i)}))
            return res
        except Exception as e:
            conn.rollback()
            raise e

    @classmethod
    def count(cls, where='0=0'):
        s, conn = get_session()
        try:
            sql = f"""
                select count(*) from {cls.table_name} where {where};
            """
            if cls.is_log:
                print(sql)
            s.execute(sql)
            db_res = s.fetchone()
            return db_res[0]
        except Exception as e:
            conn.rollback()
            raise e

    @classmethod
    def get_one(cls,order_by='id desc', where='0=0'):
        s, conn = get_session()
        try:
            sql = f"""
                    select `{'`,`'.join(cls.fields)}` 
                    from {cls.table_name} 
                    where {where}
                    order by {order_by}
                   """
            if cls.is_log:
                print(sql)
            s.execute(sql)
            db_res = s.fetchone()
            if not db_res:
                return None
            return cls.format(**{k: v for k, v in zip(cls.fields, db_res)})
        except Exception as e:
            conn.rollback()
            raise e

    @classmethod
    def get_by_id(cls, id):
        s, conn = get_session()
        try:
            sql = f"""
                    select `{'`,`'.join(cls.fields)}` 
                    from {cls.table_name} 
                    where id={id};
                   """
            if cls.is_log:
                print(sql)
            s.execute(sql)
            db_res = s.fetchone()
            if not db_res:
                return None
            return cls.format(**{k: v for k, v in zip(cls.fields, db_res)})
        except Exception as e:
            conn.rollback()
            raise e

    @classmethod
    def update_by_id(cls, id, **kwargs):
        s, conn = get_session()
        try:
            sql = f"""
                update `{cls.table_name}` 
                set {', '.join([f'`{k}`={value_format(v)}' for k, v in kwargs.items()])}
                where id={id};
            """
            if cls.is_log:
                print(sql)
            s.execute(sql)
            conn.commit()
            return cls.get_by_id(id)
        except Exception as e:
            conn.rollback()
            raise e

    @classmethod
    def delete_by_id(cls, id):
        s, conn = get_session()
        try:
            sql = f"""
                delete from {cls.table_name} where id={id}
            """
            if cls.is_log:
                print(sql)
            s.execute(sql)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e

    def __str__(self):
        return self.table_name+" ; ".join([f"{i}={getattr(self, i)}" for i in self.fields])


class User(BaseModel):
    fields = [
        'id',
        'first_name',
        'last_name',
        'address',
        'email',
        'date_of_birth',
        'pass_hash',
        'phone_number',
        'is_staff',
        'is_manager',
        'is_admin',
        'date_joined',
        'gift_card'
    ]

    id: int | None
    first_name: str | None
    last_name: str | None
    address: str | None
    email: str | None
    date_of_birth: date | None
    pass_hash: str | None
    phone_number: str | None
    is_staff: bool | None
    is_manager: bool | None
    is_admin: bool | None
    date_joined: date | None
    gift_card: float | None


    table_name = 'user'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.first_name = kwargs.get('first_name', None)
        self.last_name = kwargs.get('last_name', None)
        self.address = kwargs.get('address', None)
        self.email = kwargs.get('email', None)
        self.date_of_birth = kwargs.get('date_of_birth', None)
        self.pass_hash = kwargs.get('pass_hash', None)
        self.phone_number = kwargs.get('phone_number', None)
        self.date_joined = kwargs.get('date_joined', None)
        self.is_staff = bool(kwargs.get('is_staff', 0))
        self.is_admin = bool(kwargs.get('is_admin', 0))
        self.is_manager = bool(kwargs.get('is_manager', 0))
        self.id = kwargs.get('id', None)
        self.gift_card = kwargs.get('gift_card', None)

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

if User.get_any(where="email = 'admin@test.com'").__len__() == 0:
    User.create(
        first_name='test',
        last_name='admin',
        email='admin@test.com',
        pass_hash=generate_password_hash('admin_pass'),
        is_admin=True,
        phone_number='12334567'
    )
if User.get_any(where="email = 'staff@test.com'").__len__() == 0:
    User.create(
        first_name='test',
        last_name='staff',
        email='staff@test.com',
        pass_hash=generate_password_hash('staff_pass'),
        is_staff=True,
        phone_number='1233456'
    )
if User.get_any(where="email = 'manager@test.com'").__len__() == 0:
    User.create(
        first_name='test',
        last_name='manager',
        email='manager@test.com',
        pass_hash=generate_password_hash('staff_pass'),
        is_manager=True,
        phone_number='123345678'
    )

class GiftCardLog(BaseModel):

    table_name = 'gift_card_log'

    fields = [
        'id',
        'user_id',
        'point',
        'created_at'
    ]

    id: int | None = None
    user_id: int | None = None
    point: int | None = None
    created_at: datetime | None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get('id', None)
        self.user_id = kwargs.get('user_id', None)
        self.point = kwargs.get('point', None)
        self.created_at = kwargs.get('created_at', None)


    @classmethod
    def get_total_money(cls,where='0=0') -> float:
        s, conn = get_session()
        try:
            sql = f'''
                select sum(point) from {cls.table_name} where {where}
            '''
            s.execute(sql)
            if cls.is_log:
                print(sql)
            return s.fetchone()[0]
        except Exception as e:
            conn.rollback()
            raise e

class Movie(BaseModel):
    fields = [
        'id',
        'title',
        'original_language',
        'overview',
        'poster_path',
        'release_date',
        'duration_min'
    ]

    id: int | None
    title: str | None
    original_language: str | None
    overview: str | None
    poster_path: str | None
    release_date: datetime | None
    duration_min: float | None


    table_name = 'movie'

    @property
    def screenings(self) -> list['Screening']:
        screenings = []
        if self.id is not None:
            screenings = Screening.get_any(limit=999, order_by='start_date_time desc',where=f"movie_id={self.id}")
        return screenings

    @property
    def now_screenings(self) -> list['Screening']:
        screenings = []
        if self.id is not None:
            screenings = Screening.get_any(limit=999, where=f"movie_id={self.id} and TIMESTAMP(start_date_time) > TIMESTAMP(NOW()) and DATE(start_date_time) = DATE(NOW())")
        return screenings

    @property
    def get_dates(self):
        s, conn = get_session()
        try:
            sql = f"select DATE(start_date_time) from screening where movie_id = {self.id} and TIME(start_date_time) > TIME(NOW()) and DATE(start_date_time) = DATE(NOW()) group by DATE(start_date_time)"
            s.execute(sql)
            if self.is_log:
                print(sql)
            return [i[0].strftime('%Y-%m-%d') for i in s.fetchall() if i is not None]
        except Exception as e:
            print(e)
            raise e

    @property
    def movie_types(self):
        s, conn = get_session()
        res = []
        try:
            sql = f"SELECT name FROM genre where id in (select id from movie_genre where movie_id = {self.id})"
            s.execute(sql)
            if self.is_log:
                print(sql)
            res = [i[0] for i in s.fetchall()]
        except Exception as e:
            conn.rollback()
            raise e
        return res

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = kwargs.get('title', None)
        self.original_language = kwargs.get('original_language', None)
        self.overview = kwargs.get('overview', None)
        self.poster_path = kwargs.get('poster_path', None)
        self.release_date = kwargs.get('release_date', None)
        self.duration_min = kwargs.get('duration_min', None)
        self.id = kwargs.get('id', None)  # Assuming -1 as default value for ID if not provided


class Genre(BaseModel):
    fields = [
        'id',
        'name'
    ]

    id: int | None
    name: str | None

    table_name = 'genre'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.get('name', None)
        self.id = kwargs.get('id', None)  # Assuming -1 as default value for ID if not provided


class MovieGenre(BaseModel):
    fields = [
        'id',
        'movie_id',
        'genre_id'
    ]

    id: int | None
    movie_id: int | None
    genre_id: int | None

    table_name = 'movie_genre'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.movie_id = kwargs.get('movie_id', None)
        self.genre_id = kwargs.get('genre_id', None)
        self.id = kwargs.get('id', None)  # Assuming -1 as default value for ID if not provided


class Hall(BaseModel):
    fields = [
        'id',
        'name',
        'number_of_seats',
        'number_of_columns'
    ]

    id: int | None
    name: str | None
    number_of_seats: int | None
    number_of_columns: int | None

    table_name = 'hall'

    @property
    def today_screenings(self) -> list['Screening']:
        screenings = []
        if self.id is not None:
            screenings = Screening.get_any(limit=999,
                                           where=f"hall_id={self.id} and  start_date_time > NOW() AND DATE(start_date_time) = CURDATE()")
        return screenings

    def get_seats(self) -> list['Seat']:
        seats = []
        if self.id is not None:
            seats = Seat.get_any(limit=999, where=f"hall_id={self.id} ")
        return seats

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.number_of_seats = kwargs.get('number_of_seats', None)
        self.number_of_columns = kwargs.get('number_of_columns', None)
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)


class Screening(BaseModel):
    fields = [
        'id',
        'movie_id',
        'start_date_time',
        'end_date_time',
        'hall_id',
        'available_seats',
        'adult_price',
        'child_price',
        'student_price',
        'senior_price'
    ]

    id: int | None
    movie_id: int | None
    start_date_time: datetime | None
    end_date_time: datetime | None
    hall_id: int | None
    available_seats: int | None
    adult_price: float | None
    child_price: float | None
    student_price: float | None
    senior_price: float | None

    table_name = 'screening'

    @property
    def movie(self) -> Movie | None:
        if self.movie_id is None:
            return None
        else:
            return Movie.get_by_id(self.movie_id)

    @property
    def get_hall(self) -> Hall | None:
        if self.hall_id is None:
            return None
        else:
            return Hall.get_by_id(self.hall_id)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.movie_id = kwargs.get('movie_id', None)
        self.start_date_time = kwargs.get('start_date_time', None)
        self.end_date_time = kwargs.get('end_date_time', None)
        self.hall_id = kwargs.get('hall_id', None)
        self.available_seats = kwargs.get('available_seats', None)
        self.senior_price = kwargs.get('senior_price', None)
        self.child_price = kwargs.get('child_price', None)
        self.student_price = kwargs.get('student_price', None)
        self.adult_price = kwargs.get('adult_price', None)
        self.id = kwargs.get('id', None)


class Coupon(BaseModel):
    table_name = 'coupon'

    fields = [
        'id',
        'code',
        'title',
        'remark',
        'discount',
        'expiry_date',
        'is_active',
        'used_counter',
        'use_limit'
    ]

    id: int | None
    code: str | None
    title: str | None
    remark: str | None
    discount: float | None
    expiry_date: datetime | None
    is_active: bool | None
    used_counter: int | None
    use_limit: int | None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.code = kwargs.get('code', None)
        self.discount = kwargs.get('discount', None)
        self.expiry_date = kwargs.get('expiry_date', None)
        self.is_active = kwargs.get('is_active', None)
        self.used_counter = kwargs.get('used_counter', None)
        self.title = kwargs.get('title', None)
        self.remark = kwargs.get('remark', None)
        self.use_limit = kwargs.get('use_limit', None)
        self.id = kwargs.get('id', None)


class Seat(BaseModel):
    table_name = 'seat'

    fields = [
        'id',
        'hall_id',
        'seat_id_in_hall',
        'row',
        'col',
        'type',
        'price'
    ]

    id: int | None
    hall_id: int | None
    seat_id_in_hall: int | None
    row: int | None
    col: int | None
    type: int | None
    price: float | None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hall_id = kwargs.get('hall_id', None)
        self.seat_id_in_hall = kwargs.get('seat_id_in_hall', None)
        self.row = kwargs.get('row', None)
        self.col = kwargs.get('col', None)
        self.type = kwargs.get('type', None)
        self.price = kwargs.get('price', None)
        self.id = kwargs.get('id', None)


class Booking(BaseModel):
    table_name = 'booking'

    fields = [
        'id',
        'user_id',
        'created_date_time',
        'status',
        'screening_id',
        'seats',
        'price_total',
        'payment_id'
    ]

    user_id: int | None
    created_date_time: datetime | None
    status: int | None
    screening_id: int | None
    seats: list | None
    price_total: float | None
    payment_id: int | None

    @property
    def payment(self):
        return Payment.get_by_id(self.payment_id)

    @property
    def screening(self) -> Screening:
        return Screening.get_by_id(self.screening_id)

    @classmethod
    def get_ticket(cls, where='0=0'):
        s, conn = get_session()
        try:
            sql = f"select SUM(JSON_LENGTH(seats)) from booking where screening_id in (select id from screening where {where})"
            s.execute(sql)
            if cls.is_log:
                print(sql)
            return s.fetchone()[0]
        except Exception as e:
            conn.rollback()
            raise e

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = kwargs.get('user_id', None)
        self.created_date_time = kwargs.get('created_date_time', None)
        self.status = kwargs.get('status', None)
        self.screening_id = kwargs.get('screening_id', None)
        self.seats = kwargs.get('seats', None)
        self.price_total = kwargs.get('price_total', None)
        self.payment_id = kwargs.get('payment_id', None)
        self.id = kwargs.get('id', None)


class Payment(BaseModel):
    table_name = 'payment'

    fields = [
        'id',
        'user_id',
        'booking_id',
        'payment_date_time',
        'payment_method',
        'coupon_id',
        'amount',
        'final_amount'
    ]

    id: int | None
    booking_id: int | None
    payment_date_time: datetime | None
    payment_method: str | None
    coupon_id: int | None
    amount: float | None
    final_amount: float | None
    user_id: int | None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.booking_id = kwargs.get('booking_id', None)
        self.payment_date_time = kwargs.get('payment_date_time', None)
        self.payment_method = kwargs.get('payment_method', None)
        self.coupon_id = kwargs.get('coupon_id', None)
        self.amount = kwargs.get('amount', None)
        self.final_amount = kwargs.get('final_amount', None)
        self.user_id = kwargs.get('user_id', None)
        self.id = kwargs.get('id', None)
