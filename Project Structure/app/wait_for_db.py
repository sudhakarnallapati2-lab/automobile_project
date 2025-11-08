import time
import sqlalchemy
from sqlalchemy import create_engine

DB_URL = "postgresql://postgres:admin@db:5432/testdb"

while True:
    try:
        engine = create_engine(DB_URL)
        conn = engine.connect()
        print("✅ Database is UP — starting FastAPI...")
        conn.close()
        break
    except Exception as e:
        print("⏳ Waiting for database...")
        time.sleep(2)
