import sqlite3
from datetime import datetime

conn = sqlite3.connect("fittrack.db", check_same_thread=False)
c = conn.cursor()

# ---- Create tables ----
def create_user_table():
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    name TEXT,
                    email TEXT
                )''')
    conn.commit()

def create_bmi_table():
    c.execute('''CREATE TABLE IF NOT EXISTS bmi_records (
                    name TEXT,
                    bmi REAL,
                    age INTEGER,
                    gender TEXT,
                    date TIMESTAMP
                )''')
    conn.commit()

def add_user_data(name, email):
    c.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    conn.commit()

def add_bmi_record(name, bmi, age, gender):
    now = datetime.now()
    c.execute("INSERT INTO bmi_records (name, bmi, age, gender, date) VALUES (?, ?, ?, ?, ?)",
              (name, bmi, age, gender, now))
    conn.commit()

def get_bmi_history(name):
    c.execute("SELECT date, bmi FROM bmi_records WHERE name = ? ORDER BY date", (name,))
    return c.fetchall()
