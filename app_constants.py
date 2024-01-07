
class TmdbConstants:
    tmdb_api_key = '1f54bd990f1cdfb230adb312546d765d'
    tmdb_api_key_backup = 'e55e6aab7eed25668440ac3bc8da27b5'

    tmdb_api_base_url = "https://api.themoviedb.org/3"
    tmdb_api_movie_genre_endpoint = "/genre/movie/list"
    tmdb_api_top_rated_endpoint = "/genre/movie/list"
    tmdb_poster_api_url = "https://image.tmdb.org/t/p/original/"

    poster_save_location = "static/posters/"
    movie_db_json = "static/movie_db.json"


class DBConstants:
    schema_file = "sql/db_schema.sql"
    data_fil = "sql/data.sql"
