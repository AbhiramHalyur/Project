import time
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings

while True:
    try:
        conn= psycopg2.connect(host=settings.database_hostname,database=settings.database_name,user=settings.database_username,
        password=settings.database_password,cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break

    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(2)