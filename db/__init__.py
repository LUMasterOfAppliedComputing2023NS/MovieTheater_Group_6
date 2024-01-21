import mysql
from mysql.connector import MySQLConnection

import config

conn = mysql.connector.connect(
    user=config.db_user,
    password=config.db_pass,
    host=config.db_host,
    database=config.db_name,
    port=config.db_port,
    autocommit=True
)


def get_session():
    return conn.cursor(), conn
