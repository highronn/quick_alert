from peewee import (
    MySQLDatabase
)


db = dev_db = MySQLDatabase(
    'quickalert',
    user='quickalert', password='quickalert',
    host='127.0.0.1', port=3306
)
