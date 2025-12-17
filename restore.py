import shutil
import json
import os
from pathlib import Path

# --- CONFIGURATION ---
# Make sure this matches the path in your janitor.py
TARGET_FOLDER = Path("C:/Users/Maureennkwocha/OneDrive - Federal University of Technology, Owerri/Documents") 
DELETE_FOLDER = TARGET_FOLDER / "_TO_DELETE_REVIEW"
RESTORE_LOG = DELETE_FOLDER / "restore_map.json"

def get_history():
    """Loads the history map safely."""
    if not RESTORE_LOG.exists():
        return {}
    try:
        with open(RESTORE_LOG, 'r') as f:
            return json.load(f)
    except:
        return {}

def restore_by_filename(filename, history):
    """Restores a single file using the history map."""
    # Check if we know where this file belongs
    if filename not in history:
        print(f"⚠  Error: No record found for where '{filename}' belongs.")
        return

    original_path = Path(history[filename])
    current_location = DELETE_FOLDER / filename

    # Move it back
    if current_location.exists():
        try:
            # Ensure the parent folder (e.g., Downloads) still exists
            original_path.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.move(str(current_location), str(original_path))
            print(f"✅ Success! Restored to: {original_path}")
            
            # Remove from history and save
            del history[filename]
            with open(RESTORE_LOG, 'w') as f:
                json.dump(history, f, indent=4)
                
        except Exception as e:
            print(f"❌ Error moving file: {e}")
    else:
        print(f"❌ Error: File '{filename}' is missing from the delete folder.")

def main():
    if not DELETE_FOLDER.exists():
        print(f"Delete folder not found: {DELETE_FOLDER}")
        return

    # Loop so you can restore multiple files without restarting the script
    while True:
        # Get list of files, excluding the log file and hidden system files
        files = [
            f.name for f in DELETE_FOLDER.iterdir() 
            if f.is_file() and f.name != "restore_map.json" and not f.name.startswith(".")
        ]

        if not files:
            print("\n--- Quarantine is empty. Nothing to restore! ---")
            break

        print("\n--- Files in Quarantine ---")
        # Enumerate gives us a counter (index) starting at 1
        for index, file in enumerate(files, start=1):
            print(f"[{index}] {file}")
        
        print("\nType the NUMBER to restore, or 'q' to quit.")
        choice = input("> ").strip().lower()

        if choice == 'q':
            print("Exiting.")
            break

        # Validate Input
        try:
            selection_index = int(choice) - 1 # Convert to 0-based index
            
            if 0 <= selection_index < len(files):
                file_to_restore = files[selection_index]
                history = get_history()
                restore_by_filename(file_to_restore, history)
            else:
                print("⚠  Invalid number selected. Please try again.")
        
        except ValueError:
            print("⚠  Please enter a valid number.")

if __name__ == "__main__":
    main()