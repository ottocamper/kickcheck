#!/usr/bin/env python3
"""
Initialize the KickCheck SQLite database
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'kickcheck.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')

def init_database():
    """Initialize the database with schema"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Read and execute schema
    with open(SCHEMA_PATH, 'r') as f:
        schema = f.read()
        cursor.executescript(schema)
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

if __name__ == '__main__':
    init_database()

