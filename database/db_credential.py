class DbCredential:
    def __init__(self, db_user: str, db_pass: str, db_host: str, db_port, db_name: str):
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name

    def __str__(self):
        return f"DbCredential - db_user:{self.db_user} db_host:{self.db_host}:{self.db_port} db_name:{self.db_name}"
