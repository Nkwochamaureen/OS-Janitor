import os
import shutil
import time
import json
import argparse
from pathlib import Path

# --- CONFIGURATION ---
DEFAULT_DAYS = 30

def setup(delete_folder, restore_log):
    """Ensures quarantine folder and log exist."""
    delete_folder.mkdir(exist_ok=True)
    if not restore_log.exists():
        with open(restore_log, 'w') as f:
            json.dump({}, f)

def get_history(restore_log):
    try:
        with open(restore_log, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_history(history, restore_log):
    with open(restore_log, 'w') as f:
        json.dump(history, f, indent=4)

def is_old(filepath, days_threshold):
    now = time.time()
    file_mod_time = os.path.getmtime(filepath)
    days_old = (now - file_mod_time) / (24 * 3600)
    return days_old > days_threshold

# --- PART 1: THE CLEANER ---
def run_cleaner(target_folder, delete_folder, restore_log, days):
    print(f"--- 🧹 Scanning {target_folder.name} for files older than {days} days ---")
    setup(delete_folder, restore_log)
    history = get_history(restore_log)
    count = 0

    for item in target_folder.iterdir():
        # Skip folders and the delete folder itself
        if item.is_dir() or item.name == "_TO_DELETE_REVIEW":
            continue

        if is_old(item, days):
            # Record original location
            history[item.name] = str(item.absolute())
            
            # Move the file
            try:
                shutil.move(str(item), str(delete_folder / item.name))
                print(f"   -> Moved to quarantine: {item.name}")
                count += 1
            except Exception as e:
                print(f"   ❌ Error moving {item.name}: {e}")

    save_history(history, restore_log)
    if count == 0:
        print("   (No new old files found)")
    else:
        print(f"--- Moved {count} files to quarantine ---")

# --- PART 2: THE RESTORER ---
def restore_file(filename, delete_folder, restore_log):
    history = get_history(restore_log)
    
    if filename not in history:
        print(f"⚠  Unknown origin for '{filename}'. Cannot auto-restore.")
        return

    original_path = Path(history[filename])
    current_location = delete_folder / filename

    if current_location.exists():
        try:
            original_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(current_location), str(original_path))
            print(f"✅ Restored: {filename}")
            
            del history[filename]
            save_history(history, restore_log)
        except Exception as e:
            print(f"❌ Error restoring file: {e}")
    else:
        print(f"❌ File not found in quarantine.")

# --- PART 3: THE TERMINATOR ---
def delete_remaining_files(delete_folder, restore_log):
    """Permanently deletes everything left in the quarantine folder."""
    files = [f for f in delete_folder.iterdir() if f.name != "restore_map.json" and not f.name.startswith(".")]
    
    if not files:
        print("Quarantine is already empty.")
        return

    print(f"\n🚨 WARNING: You are about to permanently delete {len(files)} files.")
    confirm = input("Are you sure? (Type 'yes' to confirm): ").strip().lower()
    
    if confirm == 'yes':
        for f in files:
            try:
                if f.is_file():
                    os.remove(f)
                elif f.is_dir():
                    shutil.rmtree(f)
                print(f"   🗑  Deleted: {f.name}")
            except Exception as e:
                print(f"   ❌ Error deleting {f.name}: {e}")
        
        # Reset the log file since files are gone
        with open(restore_log, 'w') as f:
            json.dump({}, f)
        print("--- Cleanup Complete. Quarantine is empty. ---")
    else:
        print("Deletion cancelled. Files remain in quarantine.")

# --- MAIN INTERFACE ---
def main_interface(target_path, days):
    target_folder = Path(target_path)
    
    if not target_folder.exists():
        print(f"❌ Error: Path {target_folder} does not exist.")
        return

    delete_folder = target_folder / "_TO_DELETE_REVIEW"
    restore_log = delete_folder / "restore_map.json"

    # 1. Run the Cleaner Logic
    run_cleaner(target_folder, delete_folder, restore_log, days)

    # 2. Start the Review Loop
    while True:
        # Get list of quarantined files
        files = [
            f.name for f in delete_folder.iterdir() 
            if f.is_file() and f.name != "restore_map.json" and not f.name.startswith(".")
        ]

        if not files:
            print("\n✨ Quarantine is empty! Good job.")
            break

        print(f"\n--- 🧐 Reviewing: {len(files)} files pending deletion ---")
        for index, file in enumerate(files, start=1):
            print(f"[{index}] {file}")
        
        print("\nOPTIONS:")
        print(" [Number] : Type a number to RESTORE a file to its original folder.")
        print(" [D]      : DELETE ALL remaining files and Exit.")
        print(" [X]      : Exit without deleting (Safety Mode).")
        
        choice = input("> ").strip().lower()

        if choice == 'x':
            print("Exiting. Files are still in quarantine folder.")
            break
        
        elif choice == 'd':
            delete_remaining_files(delete_folder, restore_log)
            break

        else:
            # Try to parse as a number for restoration
            try:
                selection_index = int(choice) - 1
                if 0 <= selection_index < len(files):
                    file_to_restore = files[selection_index]
                    restore_file(file_to_restore, delete_folder, restore_log)
                else:
                    print("⚠  Invalid number.")
            except ValueError:
                print("⚠  Invalid input. Type a number, 'D', or 'X'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean folder and review files to delete.")
    parser.add_argument("--path", type=str, required=True, help="The folder to clean")
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS, help="Days until file is stale")
    
    args = parser.parse_args()
    
    main_interface(args.path, args.days)