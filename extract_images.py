import os
import re
import requests

INPUT_FILE = "./sitemap_links/pdf_urls.txt"
BASE_DIR = "Images"
VALID_IMG_EXTENSIONS = ('.png', '.jpg', '.jpeg')

# Folder categorization rules
CATEGORY_KEYWORDS = {
    "tracing-lines": "Tracing Lines",
    "missing-letters": "Missing Letters",
    "cursive-writing": "Cursive Writing",
    "letter-tracing": "Letter Tracing",
    "alphabet": "Letter Tracing",
    "number-tracing": "Number Tracing",
    "number": "Number Tracing",
    "phonics": "Phonics",
    "stickers": "Stickers",
    "flashcards": "Flashcards",
    "spot-the-difference": "Spot the Difference",
    "sliding-puzzle": "Sliding Puzzle",
    "crossword": "Crossword",
}

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def get_category_from_text(text):
    text = text.lower()
    for key, folder in CATEGORY_KEYWORDS.items():
        if key in text:
            return folder
    return "Others"

def download_image(url, folder):
    try:
        os.makedirs(folder, exist_ok=True)
        filename = url.split('/')[-1]
        filepath = os.path.join(folder, sanitize_filename(filename))
        if os.path.exists(filepath):
            print(f"  ✓ Already exists: {filepath}")
            return
        response = requests.get(url, timeout=10)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"  ✓ Downloaded: {filepath}")
    except Exception as e:
        print(f"  ✘ Failed to download {url}: {e}")

def main():
    previous_line = ""
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            url = line.strip()
            if not url:
                continue
            if url.lower().endswith(VALID_IMG_EXTENSIONS):
                combined_text = previous_line + " " + url
                category = get_category_from_text(combined_text)
                folder = os.path.join(BASE_DIR, category)
                download_image(url, folder)
            else:
                previous_line = url  # Save for next image pairing

if __name__ == "__main__":
    main()
