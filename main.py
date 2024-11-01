from model import get_tags_by_id, create_fft
from database import check_pi_connection
from config import Config
from datetime import datetime
from format_gmt import format_to_gmt
import asyncio
import aiohttp  # type: ignore
import os
import schedule  # type: ignore
import time

def save_data(data, tags):
    try:
        now = datetime.now()
        arr = []
        for i, tag in enumerate(tags):
            if "Value" not in data[i]:
                continue

            value = data[i]["Value"]
            if isinstance(value, dict):
                value = value["Value"]

            elif not isinstance(value, (str, float, int, bool)):
                value = str(value)
            
            time_stamp = format_to_gmt(now.strftime("%Y-%m-%dT%H:%M:%S"))
           
            arr.append(
                (
                    tag[0],
                    value,
                    time_stamp,
                    time_stamp
                )
            )
        create_fft(arr)

        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"Total Data saved: {len(arr)}")

    except Exception as e:
        print("An exception occurred: ", str(e))


async def send_data(urls, data):
    try:
        async with aiohttp.ClientSession() as session:
            # Ambil data selama 1 menit
            start_time = time.time()
            total_data_retrieved = 0  # Untuk menghitung total data yang diambil
            while time.time() - start_time < 60:  # 1 menit
                tasks = [fetch_data(session, url) for url in urls]  # Ambil semua URL dalam satu batch
                res = await asyncio.gather(*tasks)

                # Hitung dan simpan data
                total_data_retrieved += len(res)  # Tambahkan ke total data yang diambil
                save_data(res, data)

                print("=============================================================")

            print(f"Total data retrieved in 1 minute: {total_data_retrieved}")

    except Exception as e:
        print("An exception occurred: ", str(e))


async def fetch_data(session, url):
    username = Config.PI_SERVER_USER
    password = Config.PI_SERVER_PASSWORD

    try:
        auth = aiohttp.BasicAuth(login=username, password=password)
        async with session.get(url, auth=auth, ssl=False) as response:
            response.raise_for_status()
            data = await response.json()
            return data
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}


def jadwal_pengambilan_data():
    try:
        now = datetime.now()
        host = os.getenv("PI_SERVER_ENDPOINT")
        base_url = host + f"streams/{{}}/value?time={now}"
        
        tag_lists = get_tags_by_id(3865, 3866, 3870, 3871)
        urls = [base_url.format(tag[1]) for tag in tag_lists]

        conn = check_pi_connection()
        if conn == False:
            print("=============================================================")
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Connection failed, retrying in 10 seconds")
        else:        
            print("=============================================================")
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Start fetching data")
            
            asyncio.run(send_data(urls, tag_lists))

    except Exception as e:
        print('An exception occurred', str(e))


# Jadwalkan pengambilan data setiap hari pada waktu tertentu
schedule.every().day.at("03:00").do(jadwal_pengambilan_data)  # Ganti waktu sesuai kebutuhan

print("Jadwal pengambilan data telah diatur.")

# Menjalankan jadwal secara terus menerus
while True:
    # jadwal_pengambilan_data()
    schedule.run_pending()
    time.sleep(86400 - 60)
