# MovieTheater


### initial database setup
~~on the first launch, uncomment the following lines in controller.py to populate initial movie info in the database~~
```
    def __init__(self, db_credential: DbCredential):
        self.db_credential = db_credential
        self.db = Database(db_credential)
        # self.reset_db(
        #     recreate_db=False,
        #     load_preset_data=True,
        #     load_tmdb_movie=True,
        # )
        pass
```

Or you could just click on the red "reset database" button in the navbar.


###
To use different database credential for different environment (local vs python anywhere):
1. copy `db_connection.example.py` to `db_connection.py`
2. modify the content of `db_connection.py` with the correct credential for the environment

Note, any file with the name `db_connection_*.py` will be ignored by git (except for `db_connection.example.py`).