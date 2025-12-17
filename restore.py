import shutil
import json
import os
from pathlib import Path

# --- CONFIGURATION ---
TARGET_FOLDER = Path("C:/Users/Maureennkwocha/OneDrive - Federal University of Technology, Owerri/Documents") # Match this to janitor.py
DELETE_FOLDER = TARGET_FOLDER / "_TO_DELETE_REVIEW"
RESTORE_LOG = DELETE_FOLDER / "restore_map.json"

def restore_file(filename_to_restore):
    # 1. Load the map
    if not RESTORE_LOG.exists():
        print("No history found. Cannot auto-restore.")
        return

    with open(RESTORE_LOG, 'r') as f:
        history = json.load(f)

    # 2. Check if we know where this file belongs
    if filename_to_restore not in history:
        print(f"I don't have a record of where '{filename_to_restore}' came from.")
        return

    original_path = Path(history[filename_to_restore])
    current_location = DELETE_FOLDER / filename_to_restore

    # 3. Move it back
    if current_location.exists():
        print(f"Restoring '{filename_to_restore}' to {original_path}...")
        try:
            shutil.move(str(current_location), str(original_path))
            print("Success!")
            
            # Remove from history so the log stays clean
            del history[filename_to_restore]
            with open(RESTORE_LOG, 'w') as f:
                json.dump(history, f, indent=4)
                
        except Exception as e:
            print(f"Error moving file: {e}")
    else:
        print(f"File '{filename_to_restore}' is not in the Delete folder anymore.")

if __name__ == "__main__":
    # List available files to restore
    print("Files in quarantine:")
    if DELETE_FOLDER.exists():
        files = [f.name for f in DELETE_FOLDER.iterdir() if f.name != "restore_map.json"]
        if not files:
            print("  (Empty)")
        else:
            for f in files:
                print(f"  - {f}")
            
            print("\nType the filename you want to restore (or 'exit'):")
            user_input = input("> ").strip()
            
            if user_input.lower() != 'exit':
                restore_file(user_input)
    else:
        print("Delete folder does not exist.")