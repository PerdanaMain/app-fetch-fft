from database import getConnection
from requests import get, post
from config import Config


def get_all_tags():
    try:
        conn = getConnection()
        cur = conn.cursor()
        cur.execute("SELECT id, web_id FROM dl_ms_tag")
        tags = cur.fetchall()
        
        return tags
    except Exception as e:
      print('An exception occurred: ', e)


def create_tag(data):
    try:
      conn = getConnection()
      
      query = """
      INSERT INTO dl_value_tag_temp (tag_id, value, time_stamp, units_abbreviation, good, questionable, substituted, annotated, created_at, updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,now(),now())
      """
      
      cur = conn.cursor()
      
      cur.executemany(query,data)
      conn.commit()
      cur.close()
      
    except Exception as e:
      print('An exception occurred: ', e)
