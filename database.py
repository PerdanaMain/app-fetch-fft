import psycopg2
from config import Config
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError, Timeout, RequestException
import requests



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
            print(f"Received unexpected status code: {test_conn.status_code}")
            return False

    except ConnectionError:
        print("Error: Unable to connect to the server. The connection was lost.")
        return False
    except Timeout:
        print("Error: The request timed out.")
        return False

    except RequestException as e:
        print(f"An error occurred: {e}")
        return False