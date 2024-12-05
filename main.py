import asyncio
import aiohttp  # type: ignore
import warnings
import pytz
import uuid
import time  # For sleep functionality
from log import print_log
from datetime import datetime, timedelta
from model import *
from format_gmt import format_to_gmt
from database import check_pi_connection

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


            gen_uuid = str(uuid.uuid4())
            # Format the timestamp properly
            time_stamp = format_to_gmt(response["Timestamp"][:19])  # Adjust based on your timestamp format
            arr.append((gen_uuid, tag_id, value, time_stamp, time_stamp))

    if arr:
        create_fft(arr)
        print(f"Total Data saved: {len(arr)}")
        print_log(f"Total Data saved: {len(arr)}")

def main():
    while True:

        while True:
            conn = check_pi_connection()
            if conn == False:
                print("=============================================================")
                print(
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Connection failed, retrying in 10 seconds",
                )
            else:        
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Start fetching data")
                print("=============================================================")
                break


        now = datetime.now(pytz.timezone("Asia/Jakarta"))
        # Check if the current time is 3 AM
        if now.hour == 3 and now.minute == 0:
            tanggal = now
            end_date = tanggal + timedelta(minutes=1)

            print("Start Time: ", tanggal)

            loop = asyncio.get_event_loop()
            responses = loop.run_until_complete(gather_data(tanggal, end_date))

            # Filter out None responses
            responses = [response for response in responses if response is not None]
            print(f"Total records fetched: {len(responses)}")
            print_log(f"Total records fetched: {len(responses)}")

            # Save the fetched data into the database
            save_data(responses)

            # Sleep for 60 seconds to avoid multiple executions within the same minute
            time.sleep(60)
        else:
            print("Belum Jam 3 pagi")
            print("=============================================================")

            # Sleep for 1 minute before checking the time again
            time.sleep(60)

if __name__ == "__main__":
    main()