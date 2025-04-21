import psycopg2
from config import DB_CONFIG

def connect():
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS scan_results (
        id SERIAL PRIMARY KEY,
        ip VARCHAR(50),
        port INTEGER,
        state VARCHAR(20),
        service VARCHAR(100),
        product VARCHAR(100),
        version VARCHAR(50),
        scan_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def insert_scan_result(ip, port, state, service, product, version):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO scan_results (ip, port, state, service, product, version)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, (ip, port, state, service, product, version))
    conn.commit()
    conn.close()
