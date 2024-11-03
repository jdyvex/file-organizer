import os
import shutil
from pathlib import Path
import json
import hashlib

# Load configuration from config.json
def load_config(config_path):
    with open(config_path, 'r') as file:
        return json.load(file)

# Function to compute hash of a file
def get_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

# Function to organize files, with recursive handling for subfolders
def organize_files(directory, categories):
    for item in directory.iterdir():
        if item.is_dir():
            # Skip .app directories and any other special directories if needed
            if item.suffix == ".app":
                print(f"Skipping .app directory: {item}")
                continue
            try:
                # Recursively organize files in subdirectories
                organize_files(item, categories)
            except PermissionError as e:
                print(f"Permission error accessing directory {item}: {e}")
        elif item.is_file():
            file_ext = item.suffix.lower()  # Get the file extension
            
            # Determine the folder to move the file into
            folder_name = None
            for category, extensions in categories.items():
                if file_ext in extensions:
                    folder_name = category
                    break
            if folder_name is None:
                folder_name = "Others"  # Default folder for unrecognized files
            
            # Create the target folder in the root directory (not in subfolders)
            target_folder = directory.parent / folder_name
            target_folder.mkdir(exist_ok=True)
            
            # Move the file to the target folder in the main directory
            target_path = target_folder / item.name
            try:
                shutil.move(str(item), str(target_path))
                print(f"Moved: {item.name} -> {target_folder}")
            except PermissionError as e:
                print(f"Permission error moving file {item}: {e}")

# Function to delete empty folders, with user confirmation
def delete_empty_folders(directory):
    empty_folders = []

    # Find empty folders
    for root, dirs, files in os.walk(directory, topdown=False):
        folder = Path(root)
        if not any(folder.iterdir()):  # Check if folder is empty
            empty_folders.append(folder)

    if empty_folders:
        print("\nEmpty folders found:")
        for folder in empty_folders:
            print(f" - {folder}")

        delete_all = False
        for folder in empty_folders:
            # Ask for confirmation to delete each empty folder
            if not delete_all:
                response = input(f"\nDo you want to delete the empty folder '{folder}'? (y/n/a/skip all): ").lower()
                if response == 'y':
                    folder.rmdir()
                    print(f"Deleted folder: {folder}")
                elif response == 'a':
                    delete_all = True
                    folder.rmdir()
                    print(f"Deleted folder: {folder}")
                elif response == 'skip all':
                    print("Skipping all remaining empty folders.")
                    break
                else:
                    print(f"Skipped folder: {folder}")
            else:
                folder.rmdir()
                print(f"Deleted folder: {folder}")
    else:
        print("No empty folders found.")

# Function to detect and handle duplicate files, with user confirmation
def detect_duplicates(directory):
    file_hashes = {}
    duplicates = []

    # Traverse directory and calculate hashes, skipping .app directories
    for root, _, files in os.walk(directory):
        folder = Path(root)
        if folder.suffix == ".app":
            print(f"Skipping .app directory: {folder}")
            continue
        
        for file in files:
            file_path = folder / file
            try:
                file_hash = get_file_hash(file_path)
                if file_hash in file_hashes:
                    # Append duplicate to list
                    duplicates.append((file_hashes[file_hash], file_path))
                else:
                    file_hashes[file_hash] = file_path
            except PermissionError as e:
                print(f"Permission error accessing file {file_path}: {e}")

    # Prompt user to delete duplicates, prioritizing the original
    if duplicates:
        print("\nDuplicate files found:")
        delete_all_duplicates = False
        for original, duplicate in duplicates:
            # Ensure the "original" file is the first file in the tuple (non-copy if possible)
            if "copy" in original.name.lower() or "copy" not in duplicate.name.lower():
                original, duplicate = duplicate, original
            
            if not delete_all_duplicates:
                print(f"\nOriginal file: {original}")
                print(f"Duplicate file: {duplicate}")
                response = input("Do you want to delete this duplicate? (y/n/a/skip all): ").lower()
                if response == 'y':
                    duplicate.unlink()  # Delete duplicate
                    print(f"Deleted duplicate: {duplicate}")
                elif response == 'a':
                    delete_all_duplicates = True
                    duplicate.unlink()
                    print(f"Deleted duplicate: {duplicate}")
                elif response == 'skip all':
                    print("Skipping all remaining duplicates.")
                    break
                else:
                    print(f"Skipped duplicate: {duplicate}")
            else:
                duplicate.unlink()
                print(f"Deleted duplicate: {duplicate}")
    else:
        print("No duplicate files found.")

# Main execution
if __name__ == "__main__":
    config_path = Path(__file__).parent / 'config.json'
    config = load_config(config_path)
    
    # Set directory and categories based on configuration
    directory_to_organize = Path(config["directory"])
    file_categories = config["categories"]
    
    print("Organizing files...")
    organize_files(directory_to_organize, file_categories)
    print("File organization complete.")
    
    # Delete empty folders with user confirmation
    delete_empty_folders(directory_to_organize)
    
    # Detect and handle duplicate files with user confirmation
    detect_duplicates(directory_to_organize)
