from database import getConnection
from requests import get, post
from config import Config
from api.auth import login


def get_all_tags():
    try:
        conn = getConnection()
        cur = conn.cursor()
        cur.execute("SELECT id, web_id FROM pfi_ms_tag")
        tags = cur.fetchall()
        
        return tags
    except Exception as e:
      print('An exception occurred: ', e)


def create_tag(data):
    try:
      conn = getConnection()
      
      query = """
      INSERT INTO pfi_value_tag (tag_id, time_stamp, value, units_abbreviation, good, questionable, substituted, annotated, created_at, updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
      """
      
      cur = conn.cursor()
      
      cur.executemany(query,data)
      conn.commit()
      cur.close()
      
    except Exception as e:
      print('An exception occurred: ', e)
