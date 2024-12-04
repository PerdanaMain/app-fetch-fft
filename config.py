from dotenv import load_dotenv # type: ignore
import os

load_dotenv()

class Config:
    HOST = os.getenv("DB_HOST")
    USER = os.getenv("DB_USER")
    PASSWORD = os.getenv("DB_PASS")
    DATABASE = os.getenv("DB_NAME")
    PORT = os.getenv("DB_PORT")

    HOST_FETCH = os.getenv("DB_FETCH_HOST")
    USER_FETCH = os.getenv("DB_FETCH_USER")
    PASSWORD_FETCH = os.getenv("DB_FETCH_PASS")
    DATABASE_FETCH = os.getenv("DB_FETCH_NAME")
    PORT_FETCH = os.getenv("DB_FETCH_PORT")
    
    PI_SERVER = os.getenv("PI_SERVER_ENDPOINT")
    PI_SERVER_USER = os.getenv("PI_SERVER_USERNAME")
    PI_SERVER_PASSWORD = os.getenv("PI_SERVER_PASSWORD")
    
    API_SERVER = os.getenv("DIGITAL_TWIN_SERVER_ENDPOINT")
    API_USERNAME = os.getenv("DIGITAL_TWIN_SERVER_USERNAME")
    API_PASSWORD = os.getenv("DIGITAL_TWIN_SERVER_PASSWORD")
