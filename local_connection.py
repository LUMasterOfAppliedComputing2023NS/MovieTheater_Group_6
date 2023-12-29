from pathlib import Path
import os

from database.db_credential import DbCredential

db_credential = DbCredential(
    db_user="root", db_pass="0918", db_host='localhost', db_port="3306", db_name="movietheater"
)
