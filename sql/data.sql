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
VALUES ('SAVE20','圣诞节限定优惠券','此优惠券仅限在圣诞节期间使用，可与其它优惠活动叠加。每个账户限用一次。', 0.2, '2024-12-31 23:59:59', 1, 0, 100);
INSERT INTO coupon (code,title,remark, discount, expiry_date, is_active, used_counter, use_limit) VALUES ('WINTER20','冬季优惠券','此优惠券仅在冬季有效，适用于所有商品。每个账户限用两次。', 0.15, '2023-03-01 00:00:00', 1, 0, 200);
INSERT INTO coupon (code,title,remark, discount, expiry_date, is_active, used_counter, use_limit) VALUES ('SPRING20','春季优惠券','此优惠券仅在春季有效，适用于新上市的商品。每个账户限用一次。', 0.18, '2023-06-30 23:59:59', 1, 0, 150);
INSERT INTO coupon (code,title,remark, discount, expiry_date, is_active, used_counter, use_limit) VALUES ('SUMMER20','夏季优惠券','此优惠券仅在夏季有效，适用于防晒用品。每个账户限用三次。', 0.22, '2023-09-30 23:59:59', 1, 0, 120);
INSERT INTO coupon (code,title,remark, discount, expiry_date, is_active, used_counter, use_limit) VALUES ('HOLIDAY30','节假日优惠券','此优惠券在节假日有效，适用于所有商品。每个账户限用五次。', 0.30, '2024-09-30 23:59:59', 1, 0, 80);
INSERT INTO coupon (code,title,remark, discount, expiry_date, is_active, used_counter, use_limit) VALUES ('NEWYEAR40','元旦优惠券','此优惠券仅在元旦有效，适用于所有商品。每个账户限用四次。', 0.40, '2024-12-31 23:59:59', 1, 0, 60);
INSERT INTO coupon (code,title,remark, discount, expiry_date, is_active, used_counter, use_limit) VALUES ('MIDSUMMER50','中暑节优惠券','此优惠券仅在中暑节有效，适用于所有商品。每个账户限用六次。', 0.50, '2024-07-18 23:59:59', 1, 0, 40);
INSERT INTO coupon (code,title,remark, discount, expiry_date, is_active, used_counter, use_limit) VALUES ('LABORDAY60','劳动节优惠券','此优惠券仅在劳动节有效，适用于电子产品。每个账户限用七次。', 0.60, '2024-05-18 23:59:59', 1, 0, 30);