from model import get_all_tags, create_tag
from database import check_connection
from config import Config
from datetime import datetime, timedelta

import asyncio
import aiohttp
import os
import time


def save_data(data, tags):
    try:
        arr = []
        for i, tag in enumerate(tags):
            if "Value" not in data[i]:
                continue

            value = data[i]["Value"]
            if isinstance(value, dict):
                value = value["Value"]

            elif not isinstance(value, (str, float, int, bool)):
                value = str(value)
                
            arr.append(
                {
                    "tag_id": tag["id"],
                    "value": value,
                    "time_stamp": data[i]["Timestamp"],
                    "units_abbreviation": data[i]["UnitsAbbreviation"],
                    "good": data[i]["Good"],
                    "questionable": data[i]["Questionable"],
                    "substituted": data[i]["Substituted"],
                    "annotated": data[i]["Annotated"],
                }
            )
        create_tag(arr)

        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Data saved")

    except Exception as e:
        print("An exception occurred: ", str(e))


async def send_data(urls, data):
    try:
        async with aiohttp.ClientSession() as session:
            for i in range(0, len(urls), len(urls)):
                batch_urls = urls[i : i + len(urls)]

                tasks = [fetch_data(session, url) for url in batch_urls]
                res = await asyncio.gather(*tasks)

                print("Total response :", len(res))

                save_data(res, data)

                print("=============================================================")
                await asyncio.sleep(60)
                continue
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



def index():
    host = os.getenv("PI_SERVER_ENDPOINT")
    base_url = host + "streams/{}/value"
    

    while True:
        tag_lists = get_all_tags()
        urls = [base_url.format(tag["web_id"]) for tag in tag_lists]
        
        conn = check_connection()
        if conn == False:
            print("=============================================================")
            print(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Connection failed, retrying in 5 seconds",
            )
            time.sleep(5)
            continue
        
        print("=============================================================")
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Start fetching data")
        asyncio.run(send_data(urls, tag_lists))


if __name__ == "__main__":
    index()