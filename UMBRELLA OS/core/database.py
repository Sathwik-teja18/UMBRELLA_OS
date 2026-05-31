import os
import json
from settings import DB_FILE

def load_database():
    """Loads the Umbrella Employee Database from the local secure drive."""
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f: 
            json.dump({}, f) 
    with open(DB_FILE, 'r') as f: 
        return json.load(f)

def save_database(data):
    """Commits new employee parameters to the secure drive."""
    with open(DB_FILE, 'w') as f: 
        json.dump(data, f, indent=4)