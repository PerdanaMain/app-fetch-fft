import psycopg2 # type: ignore
from config import Config
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError, Timeout, RequestException
import requests
from datetime import datetime
import pytz



def getConnection():
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
            print("Connection successful, status code:", test_conn.status_code)
            return True
        else:
            log_disconnection(f"Received unexpected status code: {test_conn.status_code}")
            print(f"Received unexpected status code: {test_conn.status_code}")
            return False

    except ConnectionError:
        log_disconnection("Error: Unable to connect to the server. The connection was lost.")
        print("Error: Unable to connect to the server. The connection was lost.")
        return False

    except Timeout:
        log_disconnection("Error: The request timed out.")
        print("Error: The request timed out.")
        return False

    except RequestException as e:
        log_disconnection(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
        return False

def log_disconnection(message):
    # Get the current time in GMT+7
    timezone = pytz.timezone('Asia/Bangkok')  # GMT+7
    current_time = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S.%f')
    
    # Writing disconnection info to a file
    with open('logs/server_log.txt', 'a') as log_file:
        log_file.write(f"{current_time} - {message}\n")