from database import getConnection


def get_all_tags():
    query = "SELECT id, web_id FROM master_tag"

    conn = getConnection()
    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            cur.close()
            return rows
        finally:
            conn.close()


def create_tag(data):
    query = """
    INSERT INTO value_tag (tag_id, time_stamp, value, units_abbreviation, good, questionable, substituted, annotated) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""

    conn = getConnection()
    if conn is not None:
        try:
            cur = conn.cursor()
            cur.executemany(query, data)
            conn.commit()
            cur.close()
        finally:
            conn.close()
