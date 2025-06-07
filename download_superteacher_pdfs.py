import os
import re
import requests
from urllib.parse import urlparse
from pathlib import Path

INPUT_FILE = "superteacher_urls.txt"
BASE_DIR = "SuperTeacherDownloads"
VALID_EXTENSIONS = ('.pdf',)

# Categorization rules based on URL keywords
CATEGORY_KEYWORDS = {
    "addition": "Addition",
    "subtraction": "Subtraction",
    "multiplication": "Multiplication",
    "division": "Division",
    "phonics": "Phonics",
    "grammar": "Grammar",
    "reading": "Reading Comprehension",
    "word-search": "Word Search",
    "color": "Coloring",
    "mystery-picture": "Mystery Pictures",
    "math-riddle": "Math Riddles",
    "flashcards": "Flashcards",
    "task-cards": "Task Cards",
    "cut-glue": "Cut and Glue",
    "daily-math-review": "Daily Math Review",
    "puzzle": "Puzzles",
    "buzz": "Buzz Series",
    "money": "Money Math",
    "crossword": "Crossword",
    "award": "Awards",
    "decimal": "Decimals",
    "fractions": "Fractions",
    "telling-time": "Telling Time"
}

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def get_category(url):
    for key, folder in CATEGORY_KEYWORDS.items():
        if key in url:
            return folder
    return "Others"

def get_unique_filename(folder, filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(folder, new_filename)):
        new_filename = f"{base} ({counter}){ext}"
        counter += 1
    return new_filename

def download_file(url, folder):
    try:
        os.makedirs(folder, exist_ok=True)
        filename = sanitize_filename(os.path.basename(urlparse(url).path))
        filename = get_unique_filename(folder, filename)

        filepath = os.path.join(folder, filename)
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"✓ Downloaded: {filename} → {folder}")
    except Exception as e:
        print(f"✘ Failed to download {url}: {e}")

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        for line in file:
            url = line.strip()
            if not url or not url.endswith(VALID_EXTENSIONS):
                continue
            category = get_category(url)
            folder_path = os.path.join(BASE_DIR, category)
            download_file(url, folder_path)

if __name__ == "__main__":
    main()
