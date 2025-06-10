import sqlite3
import os
from datetime import datetime

# Use Render-compatible writable directory
DB_FILE = os.getenv("DB_FILE", "/tmp/contracts.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS contracts (
        id TEXT PRIMARY KEY,
        title TEXT,
        agency TEXT,
        location TEXT,
        due_date TEXT,
        summary TEXT,
        source TEXT,
        link TEXT,
        date_posted TEXT
    )''')
    conn.commit()
    conn.close()

def save_contracts(contracts):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    for contract in contracts:
        c.execute("INSERT OR REPLACE INTO contracts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (
            contract["id"],
            contract["title"],
            contract["agency"],
            contract["location"],
            contract["due_date"],
            contract["summary"],
            contract["source"],
            contract["link"],
            contract["date_posted"]
        ))
    conn.commit()
    conn.close()

def fetch_all_contracts():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM contracts ORDER BY date_posted DESC")
    rows = c.fetchall()
    conn.close()
    contracts = []
    for row in rows:
        contracts.append({
            "id": row[0],
            "title": row[1],
            "agency": row[2],
            "location": row[3],
            "due_date": row[4],
            "summary": row[5],
            "source": row[6],
            "link": row[7],
            "date_posted": row[8]
        })
    return contracts
