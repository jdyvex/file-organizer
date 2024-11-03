# File Organizer

This Python script organizes files in a specified directory based on file types.

# Usage

Simply exec `sudo python3 organizer.py` into the cmd line

## Configuration

Edit the `config.json` file to set the directory to organize and the categories.

## Usage

Simply execute `sudo python3 organizer.py` to organize your downloads folder.

```json
{
    "directory": "/path/to/your/folder",
    "categories": {
        "Images": [".jpg", ".jpeg", ".png", ".gif"],
        "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
        "Audio": [".mp3", ".wav", ".aac"],
        "Videos": [".mp4", ".mov", ".avi"],
        "Archives": [".zip", ".tar", ".gz"],
        "Others": []
    }
}
