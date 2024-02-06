import mysql
from mysql.connector import MySQLConnection

import config

conn = None

def init_conn():
    global conn
    conn = mysql.connector.connect(
            user=config.db_user,
            password=config.db_pass,
            host=config.db_host,
            database=config.db_name,
            port=config.db_port,
            autocommit=True,
            buffered=True
        )

def get_session():
    global conn
    if conn is None:
        init_conn()
    else:
        try:
            conn.ping(
                reconnect=True,
                attempts=3,
                delay=5,
            )
        except mysql.connector.InterfaceError as err:
          init_conn()

    return conn.cursor(), conn
