import datetime
from log import print_log
from database import *
from datetime import datetime

def get_all_tags():
    try:
        conn = getConnection()
        cur = conn.cursor()
        cur.execute("SELECT id, web_id FROM dl_ms_tag")
        tags = cur.fetchall()
        
        return tags
    except Exception as e:
      print(f'An exception occurred: {e}')
      print_log(f'An exception occurred: {e}')

def get_vibration_parts():
    try:
        conn = get_connection()
        cur = conn.cursor()

        query = "SELECT id, web_id, type_id, part_name  FROM pf_parts WHERE type_id = '673b26b9-fb94-40aa-8c33-ccea214c0ef3'"

        cur.execute(query)
        parts = cur.fetchall()
        return parts
    except Exception as e:
        print(f'An exception occurred: {e}')
        print_log(f'An exception occurred: {e}')
    finally:
        if conn:
            conn.close()

def get_tags_by_id(*tags_id):
    try:
        conn = getConnection()
        cur = conn.cursor()
        
        query = "SELECT id, web_id FROM dl_ms_tag WHERE id IN ({})".format(
            ','.join(['%s'] * len(tags_id))
        )
        
        cur.execute(query, tags_id)
        tags = cur.fetchall()
        
        return tags
    except Exception as e:
        print(f'An exception occurred: {e}')
        print_log(f'An exception occurred: {e}')
    finally:
        if conn:
            conn.close()


def create_fft(data):
    try:
        conn = getConnection()

        query = """
        INSERT INTO dl_fft_fetch (id, part_id, value, created_at, updated_at) VALUES (%s,%s,%s,%s,%s)
        """
        
        cur = conn.cursor()
        
        cur.executemany(query,data)
        conn.commit()
        cur.close()
      
    except Exception as e:
      print(f'An exception occurred: {e}')
      print_log(f'An exception occurred: {e}')
