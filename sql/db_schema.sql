DROP DATABASE IF EXISTS movietheater;

CREATE DATABASE IF NOT EXISTS movietheater;
USE movietheater;

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

-- 如果"movie"表不存在，则创建它
CREATE TABLE IF NOT EXISTS movie (
    -- 定义一个名为"id"的列，数据类型为整数，并设置为主键，自动递增
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    -- 定义一个名为"title"的列，数据类型为变长字符串，最大长度为255，用于存储电影的标题
    title VARCHAR(255),
    -- 定义一个名为"original_language"的列，数据类型为变长字符串，最大长度为2，用于存储电影的原语言
    original_language VARCHAR(2),
    -- 定义一个名为"overview"的列，数据类型为文本，用于存储电影的概述
    overview TEXT,
    -- 定义一个名为"poster_path"的列，数据类型为变长字符串，最大长度为255，用于存储电影海报的路径
    poster_path VARCHAR(255),
    -- 定义一个名为"release_date"的列，数据类型为日期，用于存储电影的发布日期
    release_date DATE,
    -- 定义一个名为"duration_min"的列，数据类型为整数，默认值为-1，用于存储电影的时长（分钟）
    duration_min INT default -1
);

-- 如果"genre"表不存在，则创建它
CREATE TABLE IF NOT EXISTS genre (
    -- 定义一个名为"id"的列，数据类型为整数，并设置为主键，自动递增
    id INT PRIMARY KEY AUTO_INCREMENT,
    -- 定义一个名为"name"的列，数据类型为变长字符串，最大长度为255，用于存储电影的类别名称
    name VARCHAR(255)
);

-- 如果"movie_genre"表不存在，则创建它
CREATE TABLE IF NOT EXISTS movie_genre (
    -- 定义一个名为"id"的列，数据类型为整数，并设置为自动递增
    id INT  AUTO_INCREMENT,
    -- 定义一个名为"movie_id"的列，数据类型为整数，用于存储电影的ID
    movie_id INT,
    -- 定义一个名为"genre_id"的列，数据类型为整数，用于存储类别的ID
    genre_id INT,
    -- 设置主键为"id"、"movie_id"和"genre_id"，以确保它们的唯一性
    PRIMARY KEY (id,movie_id, genre_id),
    -- 创建一个外键约束，"movie_id"列引用了"movie"表的"id"列，这意味着电影ID必须在"movie"表中存在
    FOREIGN KEY (movie_id) REFERENCES movie(id),
    -- 创建一个外键约束，"genre_id"列引用了"genre"表的"id"列，这意味着类别ID必须在"genre"表中存在
    FOREIGN KEY (genre_id) REFERENCES genre(id)
);

-- 如果"hall"表不存在，则创建它 大厅
CREATE TABLE IF NOT EXISTS hall(
    -- 定义一个名为"id"的列，数据类型为整数，并设置为主键，自动递增
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    -- 定义一个名为"name"的列，数据类型为变长字符串，最大长度为25，不能为空，用于存储大厅的名称
    name varchar(25) not null,
    -- 定义一个名为"number_of_seats"的列，数据类型为整数，不能为空，用于存储大厅的座位数
    number_of_seats INT NOT NULL,
    -- 定义一个名为"number_of_columns"的列，数据类型为整数，不能为空，用于存储大厅的列数
    number_of_columns INT NOT NULL
);

-- 如果"screening"表不存在，则创建它 放映
CREATE TABLE IF NOT EXISTS screening
(
 -- 定义一个名为"id"的列，数据类型为整数，并设置为主键，自动递增
 id INTEGER PRIMARY KEY AUTO_INCREMENT,
 -- 定义一个名为"movie_id"的列，数据类型为整数，不能为空，用于存储电影的ID
 movie_id INT NOT NULL,
 -- 定义一个名为"start_date_time"的列，数据类型为日期时间，不能为空，用于存储放映的开始时间
 start_date_time datetime Not NULL,
 -- 定义一个名为"end_date_time"的列，数据类型为日期时间，不能为空，用于存储放映的结束时间
 end_date_time  datetime Not NULL,
 -- 定义一个名为"hall_id"的列，数据类型为整数，不能为空，用于存储大厅的ID
 hall_id INT NOT NULL,
 -- 定义一个名为"available_seats"的列，数据类型为整数，不能为空，用于存储放映时剩余的可售座位数
 available_seats INT NOT NULL,
 -- 设置外键约束，"hall_id"列引用了"hall"表的"id"列，这意味着放映时的大厅ID必须在"hall"表中存在
 FOREIGN KEY (hall_id) REFERENCES hall(id),
 -- 设置外键约束，"movie_id"列引用了"movie"表的"id"列，这意味着放映的电影ID必须在"movie"表中存在
 FOREIGN KEY (movie_id) REFERENCES movie(id)
);

-- 如果"coupon"表不存在，则创建它
CREATE TABLE IF NOT EXISTS coupon (
    -- 定义一个名为"id"的列，数据类型为整数，并设置为主键，自动递增
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(64) default "",
    remark VARCHAR(255) default "",
    -- 定义一个名为"code"的列，数据类型为变长字符串，最大长度为255，不能为空，用于存储优惠券的代码
    code VARCHAR(255) NOT NULL,
    -- 定义一个名为"discount"的列，数据类型为实数，不能为空，用于存储优惠券的折扣率
    discount real NOT NULL,
    -- 定义一个名为"expiry_date"的列，数据类型为日期时间，默认值为NULL，用于存储优惠券的过期日期
    expiry_date datetime default NULL,
    -- 定义一个名为"is_active"的列，数据类型为整数，不能为空，默认值为1，用于表示优惠券是否有效（1表示有效，0表示无效）
    is_active INTEGER NOT NULL DEFAULT 1,
    -- 定义一个名为"used_counter"的列，数据类型为整数，默认值为0，用于记录优惠券的使用次数
    used_counter INT default 0,
    -- 定义一个名为"use_limit"的列，数据类型为整数，默认值为NULL，用于限制优惠券的使用次数
    use_limit INTEGER default NULL
);

-- 如果"seat"表不存在，则创建它
CREATE TABLE IF NOT EXISTS seat(
    -- 定义一个名为"id"的列，数据类型为整数，并设置为自动递增的主键
    id INTEGER AUTO_INCREMENT,
    -- 定义一个名为"hall_id"的列，数据类型为整数，不能为空，用于存储大厅的ID
    hall_id INT NOT NULL,
    -- 定义一个名为"seat_id_in_hall"的列，数据类型为整数，不能为空，用于存储大厅内的座位ID
    seat_id_in_hall INT NOT NULL,
    -- 定义一个名为"`row"`的列，数据类型为整数，不能为空，用于存储座位的行号
    `row` INT NOT NULL,
    -- 定义一个名为"`col"`的列，数据类型为整数，不能为空，用于存储座位的列号
    `col` INT NOT NULL,
    -- 定义一个名为"type"的列，数据类型为整数，不能为空，默认值为0，用于存储座位的类型（如普通座位、VIP座位等）
    type int not null default 0,
    -- 定义一个名为"price"的列，数据类型为双精度浮点数，不能为空，用于存储座位的票价
    price double not null,
    -- 设置主键为(id, hall_id, seat_id_in_hall)，确保每个座位在数据库中是唯一的
    primary key (id,hall_id, seat_id_in_hall),
    -- 设置外键约束，"hall_id"列引用了"hall"表的"id"列，这意味着座位的hall_id必须在"hall"表中存在
    FOREIGN KEY (hall_id) REFERENCES hall(id)
);


-- 如果"booking"表不存在，则创建它
CREATE TABLE IF NOT EXISTS booking(
    -- 定义一个名为"id"的列，数据类型为整数，并设置为主键，自动递增
    id INTEGER auto_increment PRIMARY KEY,
    -- 定义一个名为"user_id"的列，数据类型为整数，不能为空，用于存储用户的ID
    user_id INT NOT NULL,
    -- 定义一个名为"created_date_time"的列，数据类型为日期时间，不能为空，默认值为当前时间戳，用于存储创建日期和时间
    created_date_time datetime NOT NULL default CURRENT_TIMESTAMP,
    -- 定义一个名为"status"的列，数据类型为整数，不能为空，默认值为0，用于表示预订的状态（例如：0-待定，1-已确认，2-已取消）
    status INT NOT NULL default 0,
    -- 定义一个名为"screening_id"的列，数据类型为整数，不能为空，用于存储放映的ID
    screening_id INT NOT NULL,
    -- 定义一个名为"seats"的列，数据类型为JSON，默认值为一个空的JSON数组，用于存储预订的座位信息
    seats JSON default('[]'),
    -- 定义一个名为"price_total"的列，数据类型为双精度浮点数，不能为空，用于存储总价格
    price_total double not null,
    -- 定义一个名为"payment_id"的列，数据类型为整数，可以为空，用于存储付款的ID（如果有）
    payment_id INT default null,

    -- 设置外键约束，"user_id"列引用了"user"表的"id"列，"screening_id"列引用了"screening"表的"id"列
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (screening_id) REFERENCES screening(id)
);

-- 如果"payment"表不存在，则创建它
CREATE TABLE IF NOT EXISTS payment(
    -- 定义一个名为"id"的列，数据类型为整数，并设置为主键，自动递增
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    -- 定义一个名为"user_id"的列，数据类型为整数，不能为空，用于存储用户的ID
    user_id INT NOT NULL,
    -- 定义一个名为"booking_id"的列，数据类型为整数，不能为空，用于存储预订的ID
    booking_id INT NOT NULL,
    -- 定义一个名为"payment_date_time"的列，数据类型为日期时间，不能为空，默认值为当前时间戳，用于存储付款日期和时间
    payment_date_time datetime NOT NULL default CURRENT_TIMESTAMP,
    -- 定义一个名为"payment_method"的列，数据类型为变长字符串，最大长度为25，不能为空，用于存储付款方式（例如：信用卡、支付宝等）
    payment_method varchar(25) not null,
    -- 定义一个名为"coupon_id"的列，数据类型为整数，可以为空，用于存储优惠券的ID（如果有）
    coupon_id INT default null,
    -- 定义一个名为"amount"的列，数据类型为双精度浮点数，不能为空，用于存储付款金额
    amount double not null,
    -- 定义一个名为"final_amount"的列，数据类型为双精度浮点数，不能为空，用于存储最终付款金额（可能包含优惠券折扣等）
    final_amount double not null,
    -- 设置外键约束，"user_id"列引用了"user"表的"id"列，"coupon_id"列引用了"coupon"表的"id"列，"booking_id"列引用了"booking"表的"id"列
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (coupon_id) REFERENCES coupon(id),
    FOREIGN KEY (booking_id) REFERENCES booking(id)
);


