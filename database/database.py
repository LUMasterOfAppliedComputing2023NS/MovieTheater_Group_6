import mysql
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from database.db_credential import DbCredential


class Database:
    # connection: MySQLConnection | None = None

    def __init__(self, credential: DbCredential | None = None):
        if credential is None:
            from local_connection import db_credential
            credential = db_credential

        self.credential = credential
        self.conn: MySQLConnection | None = None
        print(f"database initialized with:{credential}")

    def init_conn(self):
        return mysql.connector.connect(
            user=self.credential.db_user,
            password=self.credential.db_pass,
            host=self.credential.db_host,
            database=self.credential.db_name,
            port=self.credential.db_port,
            autocommit=True
        )

    @property
    def cursor(self) -> MySQLCursor:
        try:
            if self.conn is None:
                raise mysql.connector.InterfaceError("conn is not established yet")

            self.conn.ping(
                reconnect=True,
                attempts=3,
                delay=5,
            )
        except mysql.connector.InterfaceError as err:
            self.conn = self.init_conn()

        return self.conn.cursor(dictionary=True)


