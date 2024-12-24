import sqlite3

def create_database():
    connection = sqlite3.connect("webhost_manager.db")
    cursor = connection.cursor()
    
    # Create clients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            website_url TEXT NOT NULL,
            login_credentials TEXT NOT NULL,
            expiry_date TEXT NOT NULL,
            domain_details TEXT,
            email_credentials TEXT,
            renewal_charges REAL
        )
    ''')
    
    # Create users table for authentication
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    connection.commit()
    connection.close()

create_database()
