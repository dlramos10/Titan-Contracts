
import sqlite3
from datetime import datetime

DB_FILE = "db/contract_data.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS contracts (
            id TEXT PRIMARY KEY,
            title TEXT,
            url TEXT,
            source TEXT,
            agency TEXT,
            publishDate TEXT,
            deadline TEXT,
            naics TEXT,
            last_updated TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_contracts(contract_list):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    for contract in contract_list:
        try:
            c.execute("INSERT OR IGNORE INTO contracts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                contract.get("id"),
                contract.get("title"),
                contract.get("url"),
                contract.get("source"),
                contract.get("agency"),
                contract.get("publishDate"),
                contract.get("deadline"),
                contract.get("naics"),
                datetime.utcnow().isoformat()
            ))
        except Exception as e:
            print("DB insert error:", e)
    conn.commit()
    conn.close()

def fetch_all_contracts():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM contracts ORDER BY publishDate DESC")
    rows = c.fetchall()
    conn.close()
    keys = ["id", "title", "url", "source", "agency", "publishDate", "deadline", "naics", "last_updated"]
    return [dict(zip(keys, row)) for row in rows]
