import psycopg
from flask import current_app

def get_connection():
    config = current_app.config['DB_CONFIG']
    return psycopg.connect(
        host=config['host'],
        port=config['port'],
        dbname=config['dbname'],
        user=config['user'],
        password=config['password']
    )
