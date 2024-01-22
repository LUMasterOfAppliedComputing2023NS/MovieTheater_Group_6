

db_user = "yana00918"
db_pass = "somerandompassword"
db_host = 'yana00918.mysql.pythonanywhere-services.com'
db_port = "3306"
db_name = "yana00918$movietheater2"

SECRET_KEY = 'secret'

'''
db_user="yana00918"
db_pass="somerandompassword"
db_host='yana00918.mysql.pythonanywhere-services.com'
db_port="3306"
db_name="yana00918$movietheater2"

mysql -h ${db_host} -u $db_user -P $db_port 'yana00918$movietheater2'
mysql -h ${db_host} -u ${db_user} -P $db_port < sql/db_schema.sql
mysql -h ${db_host} -u ${db_user} -P $db_port "${db_name}" < sql/data.sql
mysql -h ${db_host} -u $db_user -P $db_port 'yana00918$movietheater2' < sql/data.sql 
'''