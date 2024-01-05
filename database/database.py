from datetime import date
from typing import Any

import mysql
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from database.db_credential import DbCredential
from database.mapper import db_user
from model.user import User


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

    def get_items(self, table_name: str, params: dict[str, Any]):
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
        pairs = {}
        if ignore_id:
            for k, v in item.items():
                if k == 'id':
                    continue
                pairs[k] = v
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

    def delete_item_by_id(self, table: str, id: int):
        sql = f"DELETE FROM {table} WHERE id=%s"
        cursor = self.cursor
        cursor.execute(sql, (id,))
        self.conn.commit()
        pass


    def update_item(self, table_name: str, item: dict[str, Any], id: int|None = None):
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

    # specific use cases
    def create_user(self, params: dict[str, Any]):
        new_db_user = self.create_item('user', params)
        print(f"new_db_user: {new_db_user}")
        return db_user(new_db_user)

    def get_user(self, id: int) -> User|None:
        db_obj = self.get_item('user', {'id': id})
        return db_user(db_obj)
    def get_user(self, params: dict[str, Any]) -> User|None:
        db_obj = self.get_item('user', params)
        return db_user(db_obj)