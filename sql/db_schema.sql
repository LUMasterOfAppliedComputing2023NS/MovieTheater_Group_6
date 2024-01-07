# DROP DATABASE IF EXISTS movietheater;
# DROP TABLE IF EXISTS payment;
# DROP TABLE IF EXISTS movie_genre;
# DROP TABLE IF EXISTS movie;
# DROP TABLE IF EXISTS genre;
# DROP TABLE IF EXISTS screening;
# DROP TABLE IF EXISTS booking;
# DROP TABLE IF EXISTS user;
# DROP TABLE IF EXISTS seat;
# DROP TABLE IF EXISTS hall;
# DROP TABLE IF EXISTS coupon;


# CREATE DATABASE IF NOT EXISTS movietheater;
# USE movietheater;

CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT,
    address TEXT,
    email TEXT NOT NULL,
    date_of_birth DATE,
    date_joined DATE,
    pass_hash TEXT NOT NULL,
    phone_number TEXT,
    is_staff INTEGER DEFAULT 0,
    is_admin INTEGER DEFAULT 0,
    is_manager INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS movie (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255),
    original_language VARCHAR(2),
    overview TEXT,
    poster_path VARCHAR(255),
    release_date DATE,
    duration_min INT default -1
);

CREATE TABLE IF NOT EXISTS genre (
    id INT PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS movie_genre (
    movie_id INT,
    genre_id INT,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movie(id),
    FOREIGN KEY (genre_id) REFERENCES genre(id)
);

CREATE TABLE IF NOT EXISTS hall(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name varchar(25) not null,
    number_of_seats INT NOT NULL,
    number_of_columns INT NOT NULL
);

CREATE TABLE IF NOT EXISTS screening
(
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
    movie_id INT NOT NULL,
	start_date_time datetime Not NULL,
	end_date_time  datetime Not NULL,
    hall_id INT NOT NULL,
    available_seats INT NOT NULL,
	FOREIGN KEY (hall_id) REFERENCES hall(id),
	FOREIGN KEY (movie_id) REFERENCES movie(id)
);


CREATE TABLE IF NOT EXISTS booking(
    id INTEGER auto_increment PRIMARY KEY,
    user_id INT NOT NULL,
    created_date_time datetime NOT NULL default CURRENT_TIMESTAMP,
    status INT NOT NULL default 0,
    screening_id INT NOT NULL,
    price_total double not null,
    payment_id INT default null,

    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (screening_id) REFERENCES screening(id)
);

CREATE TABLE IF NOT EXISTS seat (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    booking_id INT NOT NULL,
    seat_number INT NOT NULL,
    row INT NOT NULL,
    col INT NOT NULL,
    type int not null default 0,
    price double not null,
    FOREIGN KEY (booking_id) REFERENCES booking(id)
);

CREATE TABLE IF NOT EXISTS coupon (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(255) NOT NULL,
    discount real NOT NULL,
    expiry_date datetime default NULL,
    is_active INTEGER NOT NULL DEFAULT 1,
    used_counter INT default 0,
    use_limit INTEGER default NULL
);



CREATE TABLE IF NOT EXISTS payment(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    booking_id INT NOT NULL,
    payment_date_time datetime NOT NULL default CURRENT_TIMESTAMP,
    payment_method varchar(25) not null,
    coupon_id INT default null,
    amount double not null,
    final_amount double not null,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (coupon_id) REFERENCES coupon(id),
    FOREIGN KEY (booking_id) REFERENCES booking(id)
);




