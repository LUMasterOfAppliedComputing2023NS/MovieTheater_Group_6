/*
 Navicat Premium Data Transfer

 Source Server         : yana
 Source Server Type    : MySQL
 Source Server Version : 80034 (8.0.34)
 Source Host           : 172.16.11.155:3306
 Source Schema         : comp639

 Target Server Type    : MySQL
 Target Server Version : 80034 (8.0.34)
 File Encoding         : 65001

 Date: 06/12/2023 12:55:20
*/


-- ----------------------------
-- Table structure for user
-- ----------------------------
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `pass_hash` varchar(255) NOT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `is_staff` int DEFAULT '0',
  `is_admin` int DEFAULT '0',
  `is_manager` int DEFAULT '0',
  PRIMARY KEY (`id`)
);

-- ----------------------------
-- Table structure for movies
-- ----------------------------
CREATE TABLE `movie` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `description` varchar(255) NOT NULL,
  `running_time` int DEFAULT NULL,
  `release_date` int DEFAULT NULL,
  `maximum_occupancy` int DEFAULT NULL,
  `rental_per_night` decimal(10,2) DEFAULT NULL,
  `house_image` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ----------------------------
-- Table structure for genres
-- ----------------------------
CREATE TABLE genres (
    id INT PRIMARY KEY,
    name VARCHAR(255)
);

-- ----------------------------
-- Table structure for coupon
-- ----------------------------
DROP TABLE IF EXISTS "coupon";
CREATE TABLE IF NOT EXISTS coupon (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(255) NOT NULL,
    discount real NOT NULL,
    expiry_date datetime default NULL,
    is_active INTEGER NOT NULL DEFAULT 1,
    used_counter INT default 0,
    use_limit INTEGER default NULL
);

-- ----------------------------
-- Table structure for payment
-- ----------------------------
DROP TABLE IF EXISTS "payment";
CREATE TABLE payment(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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