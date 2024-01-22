-- DROP DATABASE IF EXISTS movietheater;
-- CREATE DATABASE IF NOT EXISTS movietheater;
-- USE movietheater;


DROP DATABASE IF EXISTS yana00918$movietheater2;
CREATE DATABASE IF NOT EXISTS yana00918$movietheater2;
USE yana00918$movietheater2;

create table coupon
(
    id           int auto_increment
        primary key,
    title        varchar(64)  default '' null,
    remark       varchar(255) default '' null,
    code         varchar(255)            not null,
    discount     double                  not null,
    expiry_date  datetime                null,
    is_active    int          default 1  not null,
    used_counter int          default 0  null,
    use_limit    int                     null
);

create table genre
(
    id   int auto_increment
        primary key,
    name varchar(255) null
);

create table hall
(
    id                int auto_increment
        primary key,
    name              varchar(25) not null,
    number_of_seats   int         not null,
    number_of_columns int         not null
);

create table movie
(
    id                int auto_increment
        primary key,
    title             varchar(255)   null,
    original_language varchar(2)     null,
    overview          text           null,
    poster_path       varchar(255)   null,
    release_date      date           null,
    duration_min      int default -1 null
);

create table movie_genre
(
    id       int auto_increment,
    movie_id int not null,
    genre_id int not null,
    primary key (id, movie_id, genre_id),
    constraint movie_genre_ibfk_1
        foreign key (movie_id) references movie (id),
    constraint movie_genre_ibfk_2
        foreign key (genre_id) references genre (id)
);

create index genre_id
    on movie_genre (genre_id);

create index movie_id
    on movie_genre (movie_id);

create table screening
(
    id              int auto_increment
        primary key,
    movie_id        int                        not null,
    start_date_time datetime                   not null,
    end_date_time   datetime                   not null,
    hall_id         int                        not null,
    available_seats int                        not null,
    adult_price     decimal(6, 2) default 0.00 null,
    child_price     decimal(6, 2) default 0.00 null,
    student_price   decimal(6, 2) default 0.00 null,
    senior_price    decimal(6, 2) default 0.00 null,
    constraint screening_ibfk_1
        foreign key (hall_id) references hall (id),
    constraint screening_ibfk_2
        foreign key (movie_id) references movie (id)
);

create index hall_id
    on screening (hall_id);

create index movie_id
    on screening (movie_id);

create table seat
(
    id              int auto_increment,
    hall_id         int           not null,
    seat_id_in_hall int           not null,
    row             int           not null,
    col             int           not null,
    type            int default 0 not null,
    price           double        not null,
    primary key (id, hall_id, seat_id_in_hall),
    constraint seat_ibfk_1
        foreign key (hall_id) references hall (id)
);

create index hall_id
    on seat (hall_id);

create table user
(
    id            int auto_increment
        primary key,
    first_name    text                        not null,
    last_name     text                        null,
    address       text                        null,
    email         text                        not null,
    date_of_birth date                        null,
    date_joined   date                        null,
    pass_hash     text                        not null,
    phone_number  text                        null,
    is_staff      int            default 0    null,
    is_admin      int            default 0    null,
    is_manager    int            default 0    null,
    gift_card     decimal(10, 2) default 0.00 null
);

create table gift_card_log(
    id            int auto_increment
        primary key,
    user_id           int                                not null,
    point int default  0,
    create_at datetime default CURRENT_TIMESTAMP not null,
    constraint gift_card_log_ibfk_1
        foreign key (user_id) references user (id)
);

create table booking
(
    id                int auto_increment
        primary key,
    user_id           int                                not null,
    created_date_time datetime default CURRENT_TIMESTAMP not null,
    status            int      default 0                 not null,
    screening_id      int                                not null,
    seats             json     default (_utf8mb4'[]')    null,
    price_total       double                             not null,
    payment_id        int                                null,
    constraint booking_ibfk_1
        foreign key (user_id) references user (id),
    constraint booking_ibfk_2
        foreign key (screening_id) references screening (id)
);

create index screening_id
    on booking (screening_id);

create index user_id
    on booking (user_id);

create table payment
(
    id                int auto_increment
        primary key,
    user_id           int                                not null,
    booking_id        int                                not null,
    payment_date_time datetime default CURRENT_TIMESTAMP not null,
    payment_method    varchar(25)                        not null,
    coupon_id         int                                null,
    amount            double                             not null,
    final_amount      double                             not null,
    constraint payment_ibfk_1
        foreign key (user_id) references user (id),
    constraint payment_ibfk_2
        foreign key (coupon_id) references coupon (id),
    constraint payment_ibfk_3
        foreign key (booking_id) references booking (id)
);

create index booking_id
    on payment (booking_id);

create index coupon_id
    on payment (coupon_id);

create index user_id
    on payment (user_id);

