import pymysql
from config import DB_CONFIG

try:
    conn = pymysql.connect(**DB_CONFIG)
    print("Connected to MySQL successfully!")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")