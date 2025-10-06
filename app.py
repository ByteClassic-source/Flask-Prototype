from flask import Flask, request, jsonify
from flask_cors import CORS
import json, os, hashlib

app = Flask(__name__)
CORS(app)

DATA_FILE = 'users.json'

def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(DATA_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Missing fields'}), 400

    users = load_users()

    if username in users:
        return jsonify({'error': 'Username already taken'}), 400

    for user in users.values():
        if user['email'] == email:
            return jsonify({'error': 'Email already in use'}), 400

    users[username] = {
        'email': email,
        'password': hash_password(password)
    }

    save_users(users)
    return jsonify({'success': True})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    users = load_users()

    if username in users and users[username]['password'] == hash_password(password):
        return jsonify({'success': True})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route("/")
def home():
    return "ByteChat Server is running 💌"

if __name__ == "__main__":
    app.run()

