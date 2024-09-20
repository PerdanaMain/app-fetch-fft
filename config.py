from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    HOST = os.getenv("DB_HOST")
    USER = os.getenv("DB_USER")
    PASSWORD = os.getenv("DB_PASS")
    DATABASE = os.getenv("DB_NAME")
    PI_SERVER = os.getenv("PI_SERVER_ENDPOINT")
    PI_SERVER_USER = os.getenv("PI_SERVER_USERNAME")
    PI_SERVER_PASSWORD = os.getenv("PI_SERVER_PASSWORD")
