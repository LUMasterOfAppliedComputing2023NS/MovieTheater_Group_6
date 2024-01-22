INSERT INTO user (first_name, last_name, address, email, date_of_birth, date_joined, pass_hash, phone_number, is_staff, is_admin, is_manager)
VALUES ('John', 'Doe', '123 Main St', 'john.doe@example.com', '1990-01-01', '2020-01-01', 'password_hash', '1234567890', 1, 0, 0);

INSERT INTO movie (title, original_language, overview, poster_path, release_date, duration_min)
VALUES ('Avengers: Endgame', 'EN', "Earth's Mightiest Heroes must come together and learn to fight as a team...", '/path/to/poster', '2019-04-26', 181);

INSERT INTO genre (name) VALUES ('Action');
INSERT INTO genre (name) VALUES ('Adventure');
INSERT INTO genre (name) VALUES ('Sci-Fi');

INSERT INTO movie_genre (movie_id, genre_id) VALUES (1, 1);
INSERT INTO movie_genre (movie_id, genre_id) VALUES (1, 2);
INSERT INTO movie_genre (movie_id, genre_id) VALUES (1, 3);

INSERT INTO hall (name, number_of_seats, number_of_columns)
VALUES ('Hall A', 100, 10);

INSERT INTO screening (movie_id, start_date_time, end_date_time, hall_id, available_seats)
VALUES (1, '2020-01-01 14:00:00', '2020-01-01 16:30:00', 1, 100);

INSERT INTO coupon (code,title,remark, discount, expiry_date, is_active, used_counter, use_limit)
VALUES ('SAVE20','Christmas Discount','This coupon works only during Christmas and can be used with other promotions. You can use it once per account.', 0.2, '2024-12-31 23:59:59', 1, 0, 100);
INSERT INTO coupon (code,title,remark, discount, expiry_date, is_active, used_counter, use_limit) VALUES ('WINTER20','Winter Discount','This coupon is valid only during the winter season and is applicable to all movies. Limited to two uses per account.This coupon is valid only during the winter season and is applicable to all movies. Limited to two uses per account.', 0.15, '2023-03-01 00:00:00', 1, 0, 200);
INSERT INTO coupon (code,title,remark, discount, expiry_date, is_active, used_counter, use_limit) VALUES ('SPRING20','Spring Discount','This coupon is valid only during the Spring season and is applicable to all movies. Limited to two uses per account.', 0.18, '2023-06-30 23:59:59', 1, 0, 150);
INSERT INTO coupon (code,title,remark, discount, expiry_date, is_active, used_counter, use_limit) VALUES ('SUMMER20','Summer Discount','This coupon is valid only during the Summer season and is applicable to all movies. Limited to two uses per account.', 0.22, '2023-09-30 23:59:59', 1, 0, 120);
INSERT INTO coupon (code,title,remark, discount, expiry_date, is_active, used_counter, use_limit) VALUES ('HOLIDAY30','Holiday Special','This coupon is valid only during the holiday and is applicable to all movies. Limited to one use per account.', 0.30, '2024-09-30 23:59:59', 1, 0, 80);
INSERT INTO coupon (code,title,remark, discount, expiry_date, is_active, used_counter, use_limit) VALUES ('NEWYEAR40','New Year Discount','This coupon is valid only during the New Year holiday and is applicable to all movies. Limited to two uses per account.', 0.40, '2024-12-31 23:59:59', 1, 0, 60);
INSERT INTO coupon (code,title,remark, discount, expiry_date, is_active, used_counter, use_limit) VALUES ('TUESDAY50','Tuesday Special','This coupon is valid only for Tuesday and is applicable to all movies. Limited to one use per account.', 0.50, '2024-07-18 23:59:59', 1, 0, 40);
INSERT INTO coupon (code,title,remark, discount, expiry_date, is_active, used_counter, use_limit) VALUES ('SCHOOL60','School Holiday Discount','This coupon is valid only during the winter season and is applicable to all movies. Limited to one use per account.', 0.60, '2024-05-18 23:59:59', 1, 0, 30);