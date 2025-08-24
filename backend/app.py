import os
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

# Use environment variables set by Docker Compose
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

def get_db_connection():
    # Wait for the database to be fully ready
    for _ in range(5):
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS
            )
            return conn
        except psycopg2.OperationalError as e:
            print(f"Waiting for database to start... {e}")
            time.sleep(2)
    raise Exception("Could not connect to database after several attempts.")

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE username = %s;", (username,))
        result = cur.fetchone()
        cur.close()
        
        if result and result[0] == password:
            return jsonify({"message": "Login successful!"}), 200
        else:
            return jsonify({"message": "Invalid username or password."}), 401
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"message": "Internal server error"}), 500
    finally:
        if conn:
            conn.close()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required."}), 400

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT username FROM users WHERE username = %s;", (username,))
        if cur.fetchone():
            cur.close()
            return jsonify({"message": "Username already exists."}), 409

        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s);", (username, password))
        conn.commit()
        cur.close()
        return jsonify({"message": "Registration successful! You can now log in."}), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"message": "Internal server error"}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    time.sleep(15)
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(50) NOT NULL
            );
        """)
        cur.execute("INSERT INTO users (username, password) VALUES ('devops', '12345') ON CONFLICT (username) DO NOTHING;")
        conn.commit()
        cur.close()
        print("Database initialized with sample user.")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        if conn:
            conn.close()

    app.run(host='0.0.0.0', port=5000, debug=True)

