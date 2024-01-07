import json
import os
import urllib
from pathlib import Path
from urllib.request import urlopen

from mysql.connector.cursor import MySQLCursor
from tqdm import tqdm

from app_constants import TmdbConstants

def load_tmdb_movie_genres(
        save_to_db: MySQLCursor|None = None,
        lang: str = 'en',
        base_url: str = TmdbConstants.tmdb_api_base_url,
        endpoint: str = TmdbConstants.tmdb_api_movie_genre_endpoint,
        api_key: str = TmdbConstants.tmdb_api_key,
):
    url = f"{base_url}{endpoint}?api_key={api_key}&language={lang}"
    response = urlopen(url)
    json_response = json.loads(response.read())['genres']
    return load_movie_genre(json_response, save_to_db)

def load_json_movie_genres(json_file: str,save_to_db: MySQLCursor|None = None):
    with open(json_file, 'r') as f:
        content = json.load(f)
        return load_movie_genre(content, save_to_db)


def load_movie_genre(content, save_to_db: MySQLCursor|None = None):
    genres = content if isinstance(content, list) else content['genres'] or None
    if genres is None:
        print("load movie genre failed, genres is None")
        return None
    items = []
    mapping = {}
    for i in genres:
        database_item = (i['id'], i['name'])
        items.append(database_item)
        mapping[i['id']] = i['name']

    if save_to_db is not None:
        sql = """INSERT IGNORE INTO genre (id, name) VALUES (%s, %s)"""
        save_to_db.executemany(sql, items)

        print(f"import to db success")

    return mapping

def load_movie_items(
        movies: [],
        genres: {},
        posters: [] = None,
        db: MySQLCursor|None = None,
        poster_api_host: str = TmdbConstants.tmdb_poster_api_url,
        poster_save_location: str = TmdbConstants.poster_save_location
):
    if db is not None:
        sql_movie = """INSERT IGNORE INTO movie (id, original_language, overview, poster_path, release_date, title) VALUES (%s,%s,%s,%s,%s,%s)"""
        sql_genre = """INSERT IGNORE INTO movie_genre (movie_id, genre_id) VALUES (%s,%s) """
        db.executemany(sql_movie, movies)
        # movies_changes = db.total_changes

        for (id, genres) in genres.items():
            for genre in genres:
                db.execute(sql_genre, (id, genre))
        print(f"import movies to db success, movies:{len(movies)}, genres:{len(genres)}")

        # db.commit()

    if posters is not None \
            and len(posters) != 0 \
            and poster_api_host is not None \
            and poster_save_location is not None:

        Path(poster_save_location).mkdir(parents=True, exist_ok=True)

        for i in tqdm(range(len(posters))):
            poster = posters[i]
            if not os.path.exists(f"{poster_save_location}{poster[1:]}"):
                urllib.request.urlretrieve(f"{poster_api_host}{poster}", f"{poster_save_location}{poster[1:]}")

        print(f"Downloaded all {len(posters)} poster(s)")

    pass


def get_movies_from_content(content: []):
    items = []
    genres = {}
    posters = []
    for i in content:
        poster = i['poster_path']

        database_item = (
        int(i['id']), i['original_language'], i['overview'], i['poster_path'][1:], i['release_date'], i['title'])
        items.append(database_item)
        genres[i['id']] = i['genre_ids']
        posters.append(poster)
    return items, genres, posters


def get_movies_from_json(file_path: str):
    with open(file_path, 'r') as f:
        content = json.load(f)
        if not isinstance(content, list) and content.get('results'):
            content = content['results']
    return get_movies_from_content(content)


def get_movies_from_tmdb_api(
        base_url: str = TmdbConstants.tmdb_api_base_url,
        endpoint: str = TmdbConstants.tmdb_api_top_rated_endpoint,
        page_range: [] = range(1, 5),
        api_key: str = TmdbConstants.tmdb_api_key,
):
    # https://api.themoviedb.org/3/movie/top_rated?page=2&api_key={api_key}
    full_url = f"{base_url}{endpoint}?api_key={api_key}&page="
    db_items = []
    genres = {}
    posters = []

    for page in page_range:
        url = full_url + str(page)
        print(f"Loading page {page} from url:{url} ...")
        response = urlopen(url)
        content = json.loads(response.read())['results']

        (_db_items, _genres, _posters) = get_movies_from_content(content)
        db_items.extend(_db_items)
        genres.update(_genres)
        posters.extend(_posters)
    return db_items, genres, posters


#  save content

def save_movies_from_api(
        base_url: str = "https://api.themoviedb.org/3",
        endpoint: str = "/movie/top_rated",
        page_range: [] = range(1, 5),
        api_key: str = '1f54bd990f1cdfb230adb312546d765d',
        save_to_db: MySQLCursor|None = None,
        skip_download_posters: bool = False,
        save_poster_to_location: str|None = TmdbConstants.poster_save_location,
        poster_api_host: str = TmdbConstants.tmdb_poster_api_url
):
    if skip_download_posters:
        save_poster_to_location = None

    (db_items, genres, posters) = get_movies_from_tmdb_api(base_url, endpoint, page_range, api_key)
    load_movie_items(db_items, genres, posters, save_to_db, poster_api_host, save_poster_to_location)
    return db_items, genres, posters


def save_movies_from_json(
        json_file_path: str = TmdbConstants.movie_db_json,
        save_to_db: MySQLCursor|None = None,
        skip_download_posters: bool = False,
        save_poster_to_location: str = TmdbConstants.poster_save_location,
        poster_api_host: str = TmdbConstants.tmdb_poster_api_url
):
    if skip_download_posters:
        save_poster_to_location = None
    (db_items, genres, posters) = get_movies_from_json(json_file_path)
    load_movie_items(db_items, genres, posters, save_to_db, poster_api_host, save_poster_to_location)
    return db_items, genres, posters
