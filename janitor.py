import os
import shutil
import time
from pathlib import Path

# --- CONFIGURATION ---
# Change this to the folder you want to clean (e.g., /Users/yourname/Downloads)
TARGET_FOLDER = Path("/Users/yourname/Downloads") 

# Where files go based on extension
DIRECTORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Installers": [".exe", ".dmg", ".pkg", ".deb", ".msi"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Video": [".mp4", ".mkv", ".mov", ".avi"]
}

# Folder for old files (The "Safety Net")
DELETE_REVIEW_FOLDER = TARGET_FOLDER / "_TO_DELETE_REVIEW"
DAYS_UNTIL_STALE = 30

def setup_folders():
    """Creates destination folders if they don't exist."""
    for folder in DIRECTORIES.keys():
        path = TARGET_FOLDER / folder
        path.mkdir(exist_ok=True)
    
    # Create the quarantine folder
    DELETE_REVIEW_FOLDER.mkdir(exist_ok=True)

def is_file_stale(filepath):
    """Returns True if file is older than DAYS_UNTIL_STALE."""
    # Get time now
    now = time.time()
    # Get file modification time
    file_mod_time = os.path.getmtime(filepath)
    
    # Calculate difference in days
    age_in_seconds = now - file_mod_time
    age_in_days = age_in_seconds / (24 * 3600)
    
    return age_in_days > DAYS_UNTIL_STALE

def move_file(file_path, dest_folder):
    """Moves a file to the destination safely."""
    try:
        shutil.move(str(file_path), str(dest_folder / file_path.name))
        print(f"Moved: {file_path.name} -> {dest_folder.name}")
    except shutil.Error:
        print(f"Skipped: {file_path.name} (File already exists in destination)")
    except Exception as e:
        print(f"Error moving {file_path.name}: {e}")

def run_janitor():
    print(f"--- Starting Janitor on {TARGET_FOLDER} ---")
    setup_folders()
    
    # Iterate over every item in the directory
    for item in TARGET_FOLDER.iterdir():
        # Skip if it's a directory (we only move files)
        if item.is_dir():
            continue
            
        # 1. CHECK IF STALE (Old files go to quarantine immediately)
        if is_file_stale(item):
            print(f"Found Stale File ({DAYS_UNTIL_STALE}+ days): {item.name}")
            move_file(item, DELETE_REVIEW_FOLDER)
            continue # Skip the rest of the loop for this file

        # 2. ORGANIZE BY TYPE (If not stale, sort it)
        moved = False
        file_ext = item.suffix.lower()
        
        for folder_name, extensions in DIRECTORIES.items():
            if file_ext in extensions:
                destination = TARGET_FOLDER / folder_name
                move_file(item, destination)
                moved = True
                break
        
        # Optional: Handle files that don't match any category
        if not moved:
            print(f"Ignored: {item.name} (Unknown type or too new)")

if __name__ == "__main__":
    # Check if path exists before running
    if TARGET_FOLDER.exists():
        run_janitor()
    else:
        print(f"Error: The path {TARGET_FOLDER} does not exist.")