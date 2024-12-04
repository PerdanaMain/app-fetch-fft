from config import Config
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError, Timeout, RequestException
from datetime import datetime
from log import print_log
import psycopg2 # type: ignore
import requests
import pytz

def getConnection():
    try:
        conn = psycopg2.connect(
            host=Config.HOST_FETCH,
            database=Config.DATABASE_FETCH,
            user=Config.USER,
            password=Config.PASSWORD_FETCH,
            port=Config.PORT_FETCH
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        print_log(f"Error connecting to the database: {e}")
        return None

def get_connection():
    try:
        conn = psycopg2.connect(
            host=Config.HOST,
            database=Config.DATABASE,
            user=Config.USER,
            password=Config.PASSWORD,
            port=Config.PORT
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        print_log(f"Error connecting to the database: {e}")
        return None

def check_pi_connection():
    host = Config.PI_SERVER
    username = Config.PI_SERVER_USER
    password = Config.PI_SERVER_PASSWORD
    
    try:
        test_conn = requests.get(
            host,
            auth=HTTPBasicAuth(
                username=username,
                password=password,
            ),
            verify=False,
            timeout=10,
        )
        if test_conn.status_code == 200:
            print_log(f"Connection successful, status code: {test_conn.status_code}")
            print(f"Connection successful, status code: {test_conn.status_code}")
            return True
        else:
            print_log(f"Received unexpected status code: {test_conn.status_code}")
            print(f"Received unexpected status code: {test_conn.status_code}")
            return False

    except ConnectionError:
        print_log("Error: Unable to connect to the server. The connection was lost.")
        print("Error: Unable to connect to the server. The connection was lost.")
        return False

    except Timeout:
        print_log("Error: The request timed out.")
        print("Error: The request timed out.")
        return False

    except RequestException as e:
        print_log(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
        return False

def log_disconnection(message):
    # Get the current time in GMT+7
    timezone = pytz.timezone('Asia/Bangkok')  # GMT+7
    current_time = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S.%f')
    
    # Writing disconnection info to a file
    with open('logs/server_log.txt', 'a') as log_file:
        log_file.write(f"{current_time} - {message}\n")