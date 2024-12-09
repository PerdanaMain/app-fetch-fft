import asyncio
import aiohttp  # type: ignore
import warnings
import pytz
import uuid
from datetime import datetime, timedelta
from model import *
from format_gmt import format_to_gmt
from database import check_pi_connection
import time  # For sleep functionality

warnings.filterwarnings("ignore")

# Daftar ID tag yang ingin diambil
tag_ids = get_vibration_parts()

async def fetch_data(session, url):
    username = "tjb.piwebapi"
    password = "PLNJepara@2024"
    auth = aiohttp.BasicAuth(username, password)
    
    try:
        async with session.get(url, auth=auth, ssl=False) as response:
            return await response.json()
    except Exception as e:
        print(f"Request Error for URL {url}: {e}")
        return None

async def gather_data(start_time, end_time):
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        while start_time < end_time:
            tgl = start_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

            for tag_id in tag_ids:
                url = (
                    f"https://10.47.0.54/piwebapi/streams/{tag_id[1]}/value?time={tgl}"
                )
                tasks.append(fetch_data(session, url))
                
            start_time += timedelta(milliseconds=60)  # Mengatur interval menjadi 60 ms

        responses = await asyncio.gather(*tasks)
        return responses

def save_data(responses):
    arr = []
    for i, response in enumerate(responses):
        if response and "Value" in response:
            tag_id = tag_ids[i % len(tag_ids)][0]  # Assuming tag_id is in the first element of tag_ids
            value = response["Value"]
            if isinstance(value, dict):
                value = value.get("Value", None)  # Handle case where value might be a dict

            # Format the timestamp properly
            gen_uuid = str(uuid.uuid4())
            time_stamp = format_to_gmt(response["Timestamp"][:19])  # Adjust based on your timestamp format
            arr.append((gen_uuid,tag_id, value, time_stamp, time_stamp))

    if arr:
        create_fft(arr)
        print(f"Total Data saved: {len(arr)}")


def main():
    start_date = datetime(2024, 12, 9, 3, 0)
    current_date = datetime.now()

    while True:
        # Periksa koneksi
        while True:
            conn = check_pi_connection()
            if not conn:
                print("=============================================================")
                print(
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Connection failed, retrying in 10 seconds",
                )
                time.sleep(10)
            else:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Start fetching data")
                print("=============================================================")
                break

        # Loop melalui tanggal dari start_date hingga current_date
        current_fetch_date = start_date
        while current_fetch_date <= current_date:
            start_time = current_fetch_date
            end_time = start_time + timedelta(minutes=1)

            print("Fetching data for:", start_time.strftime("%Y-%m-%d %H:%M:%S"))

            loop = asyncio.get_event_loop()
            responses = loop.run_until_complete(gather_data(start_time, end_time))

            # Filter None responses
            responses = [response for response in responses if response is not None]
            print(f"Total records fetched for {start_time}: {len(responses)}")

            save_data(responses)

            # Pindah ke pukul 3 pagi keesokan harinya
            current_fetch_date += timedelta(days=1)

        # Tunggu 60 detik sebelum eksekusi ulang
        time.sleep(60)


if __name__ == "__main__":
    main()
