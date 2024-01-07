from typing import Any

from database.database import Database
from database.db_credential import DbCredential
from database.mapper import db_user
from model.user import User


class Controller:
    currently_showing_time_hours = 2 * 24  # 2 days


    def __init__(self, db_credential: DbCredential):
        self.db = Database(db_credential)

        pass

    # region DB Management
    def reset_db(self, load_tmdb_movie: bool = False):

        pass


    def __recreate_db(self):

        pass

    def __load_tmdb_movie(self):
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
