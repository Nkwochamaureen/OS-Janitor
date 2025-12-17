import os
import shutil
import time
import json
from pathlib import Path

# --- CONFIGURATION ---
TARGET_FOLDER = Path("C:/TimeZone") # Update this path!
DELETE_FOLDER = TARGET_FOLDER / "_TO_DELETE_REVIEW"
RESTORE_LOG = DELETE_FOLDER / "restore_map.json"
DAYS_UNTIL_STALE = 0

def setup():
    DELETE_FOLDER.mkdir(exist_ok=True)
    # Create the JSON log file if it doesn't exist
    if not RESTORE_LOG.exists():
        with open(RESTORE_LOG, 'w') as f:
            json.dump({}, f)

def load_history():
    """Reads the history of where files came from."""
    try:
        with open(RESTORE_LOG, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_history(history):
    """Saves the history back to the file."""
    with open(RESTORE_LOG, 'w') as f:
        json.dump(history, f, indent=4)

def is_old(filepath):
    """Returns True if file is older than X days."""
    now = time.time()
    file_mod_time = os.path.getmtime(filepath)
    days_old = (now - file_mod_time) / (24 * 3600)
    return days_old > DAYS_UNTIL_STALE

def run_janitor():
    print(f"--- Scanning {TARGET_FOLDER} for old files ---")
    setup()
    history = load_history()
    count = 0

    for item in TARGET_FOLDER.iterdir():
        # Skip folders and the delete folder itself
        if item.is_dir() or item.name == "_TO_DELETE_REVIEW":
            continue

        if is_old(item):
            print(f"Moving Old File: {item.name}")
            
            # 1. Record original location BEFORE moving
            history[item.name] = str(item.absolute())
            
            # 2. Move the file
            try:
                shutil.move(str(item), str(DELETE_FOLDER / item.name))
                count += 1
            except Exception as e:
                print(f"Error moving {item.name}: {e}")

    # Save the map so we can restore later
    save_history(history)
    print(f"--- Done. Moved {count} files to {DELETE_FOLDER.name} ---")

if __name__ == "__main__":
    run_janitor()