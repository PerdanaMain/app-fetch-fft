import psycopg2
from config import Config


def getConnection():
    try:
        conn = psycopg2.connect(
            host=Config.HOST,
            database=Config.DATABASE,
            user=Config.USER,
            password=Config.PASSWORD,
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
