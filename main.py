from model import get_tags_by_id, create_fft
from database import check_pi_connection
from datetime import datetime, timedelta
import time
import os
import requests
from format_gmt import format_to_gmt

# Daftar tag yang akan diambil
tag_lists = get_tags_by_id(3865, 3866, 3871, 3870)

# Fungsi untuk mengambil data dari URL
import requests
from requests.auth import HTTPBasicAuth

import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

def save_data(data, tags):
    try:
        arr = []
        for tag in tags:

            value = data["Value"]

            if isinstance(value, dict) and "Value" in value:
                value = value["Value"]
            elif not isinstance(value, (str, float, int, bool)):
                value = str(value)
            time_stamp = format_to_gmt(data["Timestamp"][:19])

            arr.append((tag[0],data["Value"],data["Timestamp"],time_stamp))
        
        print(arr)

    except Exception as e:
        print("An exception occurred in save_data: ", str(e))


def fetch(urls, username, password):
    try:
        for url in urls:
            response = requests.get(url, auth=HTTPBasicAuth(username, password), verify=False)
            if response.status_code == 200:
                data = response.json()
                save_data(data, tags=tag_lists)
            else:
                print(f"Gagal mengambil data dari {url}, status code: {response.status_code}")
    except Exception as e:
        print("An exception occurred during fetch:", str(e))



def index():
    try:
        while True:
            now = datetime.now()

            while True:
                conn = check_pi_connection()
                if not conn:
                    print("=============================================================")
                    print(
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Connection failed, retrying in 10 seconds",
                    )
                    time.sleep(10)  # Retry setiap 10 detik jika koneksi gagal
                else:        
                    print("=============================================================")
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Start fetching data")
                    break


            username = os.getenv("PI_SERVER_USERNAME")
            password = os.getenv("PI_SERVER_PASSWORD")
            host = os.getenv("PI_SERVER_ENDPOINT")
            base_url = f"{host}streams/{{}}/value?time={now}"
            urls = [base_url.format(tag[1]) for tag in tag_lists]
            fetch(urls, username, password)
            
            # Cek apakah waktu sekarang adalah pukul 3 pagi
            # if now.hour == 3 and now.minute == 0:
            #     print("Mengambil data pada:", now)
                
            #     # Memanggil fungsi fetch untuk mengambil data dari URL
            #     fetch(urls)
                
            #     # Tunggu 24 jam sebelum loop berikutnya
            #     time.sleep(86400)
            # else:
            #     # Jika belum pukul 3 pagi, tunggu 1 menit sebelum cek lagi
            #     time.sleep(60)
                
    except Exception as e:
        print("An exception occurred", str(e))

if __name__ == "__main__":
    index()
