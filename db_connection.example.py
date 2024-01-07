from pathlib import Path
import os

from database.db_credential import DbCredential

# db_credential = DbCredential(
#     db_user="root", db_pass="0918", db_host='localhost', db_port="3306", db_name="movietheater"
# )
db_credential = DbCredential(
    db_user="admin", db_pass="password", db_host='172.16.2.14', db_port="3306", db_name="movietheater"
)
