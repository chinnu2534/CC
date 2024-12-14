import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('database.db')

# Create tables
conn.execute('''
CREATE TABLE IF NOT EXISTS cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    card_number TEXT,
    expiry_date TEXT,
    credit_limit REAL
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id INTEGER,
    month TEXT,
    year INTEGER,
    amount REAL,
    paid INTEGER, -- 0 for unpaid, 1 for paid
    paid_date TEXT,
    FOREIGN KEY (card_id) REFERENCES cards(id)
)
''')

conn.close()
print("Database setup completed!")
