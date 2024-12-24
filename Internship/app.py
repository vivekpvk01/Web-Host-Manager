from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def db_connection():
    connection = sqlite3.connect("webhost_manager.db")
    connection.row_factory = sqlite3.Row
    return connection

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    password = generate_password_hash(data["password"])
    
    connection = db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password))
        connection.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 409
    finally:
        connection.close()

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]
    
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    connection.close()
    
    if user and check_password_hash(user["password_hash"], password):
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/clients", methods=["POST"])
def add_client():
    data = request.json
    
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO clients (name, website_url, login_credentials, expiry_date, domain_details, email_credentials, renewal_charges)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (data["name"], data["website_url"], data["login_credentials"], data["expiry_date"], data.get("domain_details"), data.get("email_credentials"), data["renewal_charges"]))
    connection.commit()
    connection.close()
    
    return jsonify({"message": "Client added successfully"}), 201

@app.route("/clients", methods=["GET"])
def get_clients():
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM clients")
    clients = cursor.fetchall()
    connection.close()
    
    return jsonify([dict(client) for client in clients]), 200

if __name__ == "__main__":
    app.run(debug=True)
