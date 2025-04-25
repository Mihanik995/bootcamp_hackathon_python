import psycopg2
from dotenv import load_dotenv
import os

load_dotenv(encoding='utf8', verbose=True)


def execute_query(query):
    with psycopg2.connect(host=os.getenv('HOST'),
                          port=os.getenv('PORT'),
                          user=os.getenv('USER'),
                          password=os.getenv('PASSWORD'),
                          database=os.getenv('DB')) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            try:
                return cursor.fetchall()
            except Exception as e:
                pass
