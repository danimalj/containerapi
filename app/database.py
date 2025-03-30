import os
import psycopg2
from psycopg2.extras import RealDictCursor

'''DB_SETTINGS = {
    "host": os.environ["POSTGRES_HOST"],
    "port": int(os.environ["POSTGRES_PORT"]),
    "database": os.environ["POSTGRES_DB"],
    "user": os.environ["POSTGRES_USER"],
    "password": os.environ["POSTGRES_PASSWORD"],
}'
'''
DB_SETTINGS = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": int(os.getenv("POSTGRES_PORT", 5432)),
    "database": os.getenv("POSTGRES_DB", "dockdbtest"),
    "user": os.getenv("POSTGRES_USER", "api_one"),
    "password": os.getenv("POSTGRES_PASSWORD", "password_one"),
}

def get_db_connection():
    return psycopg2.connect(**DB_SETTINGS, cursor_factory=RealDictCursor)