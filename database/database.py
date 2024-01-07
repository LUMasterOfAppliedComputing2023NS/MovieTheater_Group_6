from datetime import date
from typing import Any

import mysql
from _mysql_connector import MySQLInterfaceError
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from database.db_credential import DbCredential
from database.mapper import db_user
from model.user import User


class Database:

    def __init__(self, credential: DbCredential):
        self.credential = credential
        self.__conn: MySQLConnection | None = None
        self.__cursor: MySQLCursor | None = None
        print(f"database created with:{credential}")

    def __init_conn(self):
        conn: MySQLConnection
        try:
            conn = mysql.connector.connect(
                user=self.credential.db_user,
                password=self.credential.db_pass,
                host=self.credential.db_host,
                database=self.credential.db_name,
                port=self.credential.db_port,
                autocommit=True
            )
            conn.connect()
        except MySQLInterfaceError as err:
            print(f"failed to connect to db, error: {err}")
            conn = mysql.connector.connect(
                user=self.credential.db_user,
                password=self.credential.db_pass,
                # database=self.credential.db_name,
                host=self.credential.db_host,
                port=self.credential.db_port,
                autocommit=True
            )

        conn.autocommit = True
        return conn

    @property
    def conn(self) -> MySQLConnection:
        __conn = self.__conn

        try:
            if __conn is None or not __conn.is_connected():
                raise mysql.connector.InterfaceError("conn is not established yet")

            __conn.ping(
                reconnect=True,
                attempts=3,
                delay=5,
            )
        except Exception as err:
            __conn = self.__init_conn()
            self.__conn = __conn

        return __conn

    def disconnect(self):
        __cursor = self.__cursor
        if __cursor is not None:
            __cursor.close()
            self.__cursor = None

        __conn = self.__conn
        if __conn is not None:
            __conn.commit()
            __conn.close()
            self.__conn = None

    @property
    def cursor(self, close: bool = True) -> MySQLCursor:
        __cursor = self.__cursor
        if close and __cursor is not None:
            __cursor.close()

        __cursor = self.conn.cursor(dictionary=True)
        self.__cursor = __cursor
        return __cursor

    def commit(self, block):
        try:
            conn = self.conn
            cursor = self.cursor
            block(conn, cursor)
            cursor.close()
            conn.commit()
        except Exception as err:
            print(f"failed to commit, error: {err}")
            self.conn.rollback()


    ## common use cases
    def get_item(self, table_name: str, params: dict[str, Any]):
        sql = f"SELECT * from {table_name} "
        params = params or {}

        if params is None or len(params) == 0:
            return "No input"

        conditions = []
        for k, v in params.items():
            if v is None:
                conditions.append(f"{k} = Null")
            elif isinstance(k, str):
                conditions.append(f"{k} = '{v}'")
            else:
                conditions.append(f"{k} = {v}")

        where_clause = " AND ".join(conditions)
        sql += f"WHERE {where_clause}" if conditions else ""

        cursor = self.cursor
        cursor.execute(sql)
        return cursor.fetchone()

    def get_items(self, table_name: str, params: dict[str, Any] = None):
        sql = f"SELECT * from {table_name} "
        params = params or {}

        if params is None or len(params) == 0:
            sql += ';'
        else:
            conditions = []
            for k, v in params.items():
                if v is None:
                    conditions.append(f"{k} = Null")
                elif isinstance(k, str):
                    conditions.append(f"{k} = '{v}'")
                else:
                    conditions.append(f"{k} = {v}")

            where_clause = " AND ".join(conditions)
            sql += (f"WHERE {where_clause}" if conditions else "") + ';'

        cursor = self.cursor
        cursor.execute(sql)
        return cursor.fetchall()

    def create_item(self, table_name: str, item: dict[str, Any], ignore_id: bool = True):
        pairs = item
        if ignore_id or item['id'] is None or item['id'] == -1 or item['id'] == '':
            if 'id' in item:
                del pairs['id']
        else:
            pairs = item

        placeholders = ', '.join(['%s'] * len(pairs))
        columns = "`%s`" % '`,`'.join(pairs.keys())
        sql = "INSERT INTO %s (%s) VALUES ( %s )" % (table_name, columns, placeholders)
        cursor = self.cursor
        cursor.execute(sql, list(pairs.values()))
        last_id = cursor.lastrowid
        new_item = self.get_item(table_name, {'id': last_id})
        return new_item

    def create_items(self, table_name: str, items: list[dict[str, Any]], ignore_id: bool = False):
        pairs = items
        for item in pairs:
            if ignore_id and 'id' in item:
                del pairs['id']
            elif 'id' in item and (item['id'] is None or item['id'] == -1 or item['id'] == ''):
                del item['id']

        columns = "`%s`" % '`,`'.join(pairs[0].keys())
        placeholders = ', '.join(['%s'] * len(pairs[0].keys()))
        sql = "INSERT INTO %s (%s) VALUES ( %s )" % (table_name, columns, placeholders)
        cursor = self.cursor
        cursor.executemany(sql, [list(pairs.values()) for pairs in pairs])
        cursor.close()
        self.conn.commit()
        return cursor.rowcount

    def delete_item_by_id(self, table: str, id: int):
        sql = f"DELETE FROM {table} WHERE id=%s"
        cursor = self.cursor
        cursor.execute(sql, (id,))
        self.conn.commit()
        pass

    def update_item(self, table_name: str, item: dict[str, Any], id: int | None = None):
        id = id or item['id']
        if id is None or id == '':
            return "item id not specified"

        conditions = []
        for k, v in item.items():
            if k == 'id':
                continue
            if v is None:
                conditions.append(f"{k} = NULL")
            elif isinstance(v, int):
                conditions.append(f"{k} = {v}")
            elif isinstance(v, date):
                conditions.append(f"{k} = '{v}'")
            elif isinstance(v, str) or isinstance(v, int):
                conditions.append(f"{k} = '{v}'")
            else:
                conditions.append(f"{k} = {v}")
        set_claus = ', '.join(conditions)
        sql = f"UPDATE {table_name} SET " + set_claus + " WHERE id = %s;"

        print(f"sql: {sql} table_name: {table_name} id: {id}")
        cursor = self.cursor
        cursor.execute(sql, (str(id),))
        self.conn.commit()

        rowcount = cursor.rowcount
        last_id = cursor.lastrowid

        new_item = self.get_item(table_name, {'id': id})
        print(f"updated {table_name}, rowcount:{rowcount}, last_id:{last_id}, new_item:{new_item}")
        return new_item

    # region Users
    # def create_user(self, params: dict[str, Any]):
    #     new_db_user = self.create_item('user', params)
    #     print(f"new_db_user: {new_db_user}")
    #     return db_user(new_db_user)
    #
    # def get_user_by_id(self, id: int | str) -> User | None:
    #     id = id if isinstance(id, int) else int(id)
    #     db_obj = self.get_item('user', {'id': id})
    #     return db_user(db_obj)
    #
    # def get_user(self, params: dict[str, Any]) -> User | None:
    #     db_obj = self.get_item('user', params)
    #     return db_user(db_obj)
    # endregion

    def get_movie(self, params: dict[str, Any], limit: int | None = None, offset: int | None = None):
        return self.get_item('movie', params)

    def get_showing_movies(self, limit: int | None = None, offset: int | None = None):
        sql = '''
            SELECT
                m.*,
                g.name AS genre,
                MIN(s.start_date_time) AS next_date
            FROM
                movie m
            JOIN
                movie_genre mg ON m.id = mg.movie_id
            JOIN
                genre g ON mg.genre_id = g.id
            LEFT JOIN
                screening s ON m.id = s.movie_id
            WHERE
                (s.start_date_time BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 2 DAY))
            GROUP BY
                m.title, m.release_date, g.name
            ORDER BY next_date ASC 
        '''

        if limit is not None:
            sql += f" LIMIT {limit}"

        if offset is not None:
            sql += f" OFFSET {offset}"

        sql += ';'

        cursor = self.cursor
        cursor.execute(sql)
        return cursor.fetchall()
