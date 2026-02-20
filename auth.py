import sqlite3
import hashlib

def connect_db():
    conn = sqlite3.connect("users.db")
    return conn

def create_user_table():
    conn = connect_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = connect_db()
    hashed = hash_password(password)
    try:
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = connect_db()
    hashed = hash_password(password)
    cursor = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed))
    user = cursor.fetchone()
    conn.close()
    return user
