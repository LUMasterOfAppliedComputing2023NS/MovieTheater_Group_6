import time
from datetime import datetime, timedelta
import random
# from random import random, randint
from typing import Any

from database.database import Database
from database.db_credential import DbCredential
from database.mapper import db_user
from model.user import User
from app_constants import TmdbConstants, DBConstants
from util.tmdb_util import *


class Controller:
    currently_showing_time_hours = 2 * 24  # hours
    upcoming_movies_time_hours = 14 * 24  # hours

    def __init__(self, db_credential: DbCredential):
        self.db_credential = db_credential
        self.db = Database(db_credential)
        self.__create_tables()
        # self.reset_db(
        #     recreate_db=False,
        #     load_preset_data=True,
        #     load_tmdb_movie=True,
        # )
        pass

    # region DB Management
    def reset_db(self, recreate_db: bool = True, load_preset_data: bool = True, load_tmdb_movie: bool = False):
        print("resetting db...")
        if recreate_db:
            self.__recreate_db()
            self.__create_tables()
            self.db.conn.commit()

        if load_preset_data:
            self.__load_preset_data()
            self.__create_preset_halls()
            print("preset data loaded")

        if load_tmdb_movie:
            self.__load_tmdb_movie()

        if load_preset_data:
            self.__create_preset_screenings()

        print("db reset complete")

    def __recreate_db(self, db_name: str = None):
        db_name = db_name or self.db_credential.db_name
        conn = self.db.conn
        cursor = self.db.cursor
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name};")
        cursor.execute(f"CREATE DATABASE {db_name};")
        cursor.execute(f"USE {db_name};")
        cursor.close()
        conn.commit()
        time.sleep(1)

        cursor = self.db.cursor
        cursor.execute("show databases;")
        print(f"databases:{cursor.fetchall()}")
        cursor.close()
        conn.commit()
        time.sleep(2)
        self.db.disconnect()
        print(f"db {db_name} recreated")

    def __create_tables(self):
        with open(DBConstants.schema_file, 'r') as f:
            sql = f.read().encode('utf-8')
            cursor = self.db.cursor
            cursor.execute(sql, multi=True)
            cursor.close()
            time.sleep(2)
            print(f"created tables")

        cursor = self.db.cursor
        cursor.execute("SHOW TABLES;")
        print(f"tables:{cursor.fetchall()}")
        cursor.close()
        self.db.conn.commit()

    def __load_preset_data(self):
        with open(DBConstants.data_file, 'r') as f:
            sql = f.read().encode('utf-8')
            self.db.cursor.execute(sql, multi=True)

    def __load_tmdb_movie(self, save_poster_to_location: str = None):
        genres = load_tmdb_movie_genres(save_to_db=self.db.cursor)
        movies = save_movies_from_api(save_to_db=self.db.cursor, save_poster_to_location=save_poster_to_location, page_range=range(1, 5))
        print(f"loaded genres:{len(genres)} movies:{len(movies)}")
        return genres, movies

    def __create_preset_halls(self, halls: list[dict[str, Any]] | None = None):
        halls = halls or [
            {
                'name': 'Hall 1',
                'number_of_seats': 100,
                'number_of_columns': 10,
            },
            {
                'name': 'Hall 2',
                'number_of_seats': 100,
                'number_of_columns': 10,
            },
            {
                'name': 'Hall 3',
                'number_of_seats': 100,
                'number_of_columns': 10,
            },
        ]
        self.create_halls(halls)

    def __create_preset_screenings(self, screenings: list[dict[str, Any]] | None = None):
        # cursor = self.db.cursor
        # cursor.execute("TRUNCATE TABLE booking;")
        # cursor.execute("TRUNCATE TABLE screening;")
        # cursor.close()

        movies = self.db.get_items('movie')
        halls = self.db.get_items('hall')
        movies_ids = [movie['id'] for movie in movies]
        hall_ids = [hall['id'] for hall in halls]

        now_time = datetime.now()
        delta = timedelta(days=14)
        start_date_time = now_time - delta
        end_date_time = now_time + delta

        # start from 9:00 am that day
        start_date_time = start_date_time.replace(hour=9, minute=0, second=0, microsecond=0)
        end_date_time = end_date_time.replace(hour=18, minute=0, second=0, microsecond=0)

        screenings = []
        # screenings_db = []
        for hall in halls:
            date_time = start_date_time

            while date_time < end_date_time:
                hour = date_time.hour
                movie_time = random.randint(90, 180)
                gap = random.randint(30, 60)
                if hour > 18:
                    date_time = (date_time + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)
                else:
                    if random.random() < 0.5:
                        movie = random.choice(movies_ids)
                        screening = {
                            'movie_id': movie,
                            'start_date_time': date_time,
                            'end_date_time': date_time + timedelta(minutes=movie_time),
                            'hall_id': hall['id'],
                            'available_seats': hall['number_of_seats'],
                        }

                        screenings.append(screening)

                date_time = date_time + timedelta(minutes=(gap + movie_time))

        item_count = self.db.create_items('screening', screenings)
        print(f"created {item_count} screenings")
        return screenings

        pass

    # endregion

    # region User
    def create_user(self, params: dict[str, Any]):
        new_db_user = self.db.create_item('user', params)
        print(f"new_db_user: {new_db_user}")
        return db_user(new_db_user)

    def get_user_by_id(self, id: int | str) -> User | None:
        id = id if isinstance(id, int) else int(id)
        db_obj = self.db.get_item('user', {'id': id})
        return db_user(db_obj)

    def get_user(self, params: dict[str, Any]) -> User | None:
        db_obj = self.db.get_item('user', params)
        return db_user(db_obj)

    # endregion

    def create_halls(self, halls: list[dict[str, Any]]):
        self.db.create_items('hall', halls)
        print(f"created halls: {halls}")
        pass

    def get_showing_movies(self, limit: int | None = None, offset: int | None = None):
        sql = f"""
            SELECT
                m.*,
                GROUP_CONCAT(DISTINCT g.name) AS genres,
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
                (s.start_date_time BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL {self.currently_showing_time_hours} HOUR))
            GROUP BY
                m.id
            ORDER BY next_date ASC 
        """

        if limit is not None:
            sql += f" LIMIT {limit}"

        if offset is not None:
            sql += f" OFFSET {offset}"

        sql += ';'

        cursor = self.db.cursor
        cursor.execute(sql)
        return cursor.fetchall()

    def get_upcoming_movies(self, limit: int | None = None, offset: int | None = None):
        sql = f"""
        SELECT
            m.*,
            GROUP_CONCAT(DISTINCT g.name) AS genres,
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
            (s.start_date_time BETWEEN DATE_ADD(NOW(), INTERVAL {self.currently_showing_time_hours} HOUR) AND DATE_ADD(NOW(), INTERVAL {self.upcoming_movies_time_hours} HOUR))
        GROUP BY
            m.id
        ORDER BY
            next_date ASC;

        """

        if limit is not None:
            sql += f" LIMIT {limit}"

        if offset is not None:
            sql += f" OFFSET {offset}"

        sql += ';'

        cursor = self.db.cursor
        cursor.execute(sql)
        return cursor.fetchall()