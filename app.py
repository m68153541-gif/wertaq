from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import os
import json
import logging
from datetime import datetime

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

DATA_FILE = 'users_data.json'

def load_users():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/save', methods=['POST'])
def save_user():
    data = request.json
    telegram_id = data.get('telegram_id')
    user_data = data.get('user_data')
    
    if not telegram_id or not user_data:
        return jsonify({'error': 'Missing data'}), 400
    
    users = load_users()
    users[telegram_id] = user_data
    save_users(users)
    
    return jsonify({'success': True})

@app.route('/api/load/<telegram_id>', methods=['GET'])
def load_user(telegram_id):
    users = load_users()
    user_data = users.get(telegram_id)
    
    if user_data:
        return jsonify(user_data)
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/all_users', methods=['GET'])
def all_users():
    users = load_users()
    result = []
    for uid, data in users.items():
        result.append({
            'telegram_id': uid,
            'uid': data.get('uid', '—'),
            'name': data.get('name', '—'),
            'stars': data.get('stars', 0),
            'attempts': data.get('attempts', 0),
            'bank': data.get('bank', 0)
        })
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)