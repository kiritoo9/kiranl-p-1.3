import psycopg2
import utils.logs as logs
from contextlib import contextmanager
from config.env.env import Env

@contextmanager
def db_conn():
    env = Env()

    conn = None
    try:
        conn = psycopg2.connect(
            dbname=env.DB_NAME,
            user=env.DB_USER,
            password=env.DB_PASS,
            host=env.DB_HOST,
            port=env.DB_PORT
        )
        yield conn
    except psycopg2.Error as e:
        logs.write("error", f"Database connection error: {e}")
        raise
    finally:
        if conn:
            conn.close()