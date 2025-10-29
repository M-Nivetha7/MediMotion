import os
import json
import hashlib

# File to store users’ login data
USER_DATA_FILE = "data/users.json"

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# ---------------------------
# Helper function: Hash passwords
# ---------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------------------
# Add a new user (Signup)
# ---------------------------
def add_user(username, password):
    """Adds a new user if username not taken"""
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            users = json.load(f)
    else:
        users = {}

    if username in users:
        return False  # username already exists

    users[username] = hash_password(password)
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f)
    return True

# ---------------------------
# Authenticate user (Login)
# ---------------------------
def authenticate_user(username, password):
    """Checks if the username & password are correct"""
    if not os.path.exists(USER_DATA_FILE):
        return False

    with open(USER_DATA_FILE, "r") as f:
        users = json.load(f)

    hashed = hash_password(password)
    return users.get(username) == hashed
