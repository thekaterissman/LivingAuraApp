# backend/server.py
from flask import Flask, jsonify, request
import time
import os
import random

# Initialize the Flask application
app = Flask(__name__)

# --- CORE LATTICE METRICS (Minimal Nunchi and Jeong) ---

# N: Nunchi Stream (Ambient Harmony Index - AHI)
# We simulate server load using random fluctuation around a base.
def calculate_nunchi_ahi():
    """Simulates Server Load Fluctuation (our Nunchi proxy)."""
    # Base load is 50. Nunchi is high when fluctuation is low.
    base_load = 50.0
    load_fluctuation = random.uniform(-10.0, 10.0)
    current_load = base_load + load_fluctuation
    
    # Nunchi is high if load is stable (low fluctuation)
    nunchi_score = round(100 - abs(load_fluctuation) * 5, 2)
    return {
        "load_percent": round(current_load, 2),
        "nunchi_score": max(0, nunchi_score) # Score between 0 and 100
    }

# J: Jeong Matrix (Deep Connection)
# We simulate Active User Count based on a simple in-memory tracker.
ACTIVE_USERS = set()
def calculate_jeong_connection():
    """Tracks Active User Count (our Jeong proxy)."""
    return len(ACTIVE_USERS)

# --- ENDPOINTS ---

@app.route('/', methods=['GET'])
def home_page():
    """The root endpoint serves the Living Aura's simple status page."""
    try:
        with open('index.html', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Living Aura App is Running! Frontend file not found."

@app.route('/metrics', methods=['GET'])
def get_metrics():
    """Returns the real-time Nunchi and Jeong scores."""
    nunchi_data = calculate_nunchi_ahi()
    jeong_count = calculate_jeong_connection()
    
    # This is the Living Aura Data Payload
    aura_data = {
        "timestamp": int(time.time()),
        "Nunchi_AHI": nunchi_data,
        "Jeong_Active_Users": jeong_count,
        "Aura_Status": "Resonant" if nunchi_data['nunchi_score'] > 50 else "Seeking Harmony"
    }
    return jsonify(aura_data)

@app.route('/connect', methods=['POST'])
def register_user():
    """Simulates a user connecting to track Jeong."""
    # Use a unique identifier from the request (IP or simple ID)
    user_id = request.remote_addr or str(random.randint(1000, 9999))
    ACTIVE_USERS.add(user_id)
    return jsonify({"message": f"User {user_id} connected. Jeong score updated."})

# The Gunicorn server will call this 'app' object
# if __name__ == '__main__':
#     # This block is for local testing only
#     app.run(host='0.0.0.0', port=8080)
