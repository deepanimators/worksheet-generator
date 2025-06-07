import os
import re
import requests

INPUT_FILE = "./sitemap_links/pdf_urls.txt"
BASE_DIR = "Categorised_Images"
VALID_IMG_EXTENSIONS = ('.png', '.jpg', '.jpeg')

# Expanded folder categorization rules
CATEGORY_KEYWORDS = {
    "tracing-lines": "Tracing Lines",
    "handwriting": "Handwriting Practice",
    "cursive-writing": "Cursive Writing",
    "letter-tracing": "Letter Tracing",
    "alphabet": "Letter Tracing",
    "number-tracing": "Number Tracing",
    "numbers": "Number Tracing",
    "addition": "Addition",
    "subtraction": "Subtraction",
    "multiplication": "Multiplication",
    "times-table": "Multiplication",
    "missing-numbers": "Missing Numbers",
    "counting": "Counting",
    "tally": "Counting",
    "telling-time": "Telling Time",
    "match-the-clock": "Telling Time",
    "word-search": "Word Search",
    "word-scramble": "Word Scramble",
    "rhyming": "Rhyming Words",
    "adjectives": "Adjectives",
    "verbs": "Verbs",
    "nouns": "Nouns",
    "grammar": "Grammar",
    "spelling": "Spelling Words",
    "opposite-words": "Opposite Words",
    "conjunctions": "Conjunctions",
    "homophones": "Homophones",
    "comprehension": "Comprehension",
    "prepositions": "Prepositions",
    "active-and-passive": "Active and Passive Voice",
    "action-words": "Action Words",
    "crossword": "Crossword Puzzle",
    "matching-words": "Matching Words to Pictures",
    "shadow-match": "Shadow Matching",
    "label-the-body-parts": "Body Parts",
    "find-the-same": "Find the Same",
    "fill-the-color": "Coloring",
    "coloring": "Coloring",
    "body-parts": "Body Parts",
    "five-senses": "Five Senses",
    "human-body": "Human Body",
    "animals": "Animals",
    "birds": "Birds",
    "fruits": "Fruits",
    "vegetables": "Vegetables",
    "insects": "Insects",
    "transportation": "Transportation",
    "shapes": "Shapes",
    "sports": "Sports",
    "flowers": "Flowers",
    "weather": "Weather and Seasons",
    "solar-system": "Solar System",
    "sea-animals": "Sea Animals",
    "nature": "Nature",
    "computer": "Computer & Technology",
    "technology": "Computer & Technology",
    "celebrations": "Celebrations",
    "months": "Months of the Year",
    "emotions": "Emotions / Feelings",
    "feelings": "Emotions / Feelings",
    "character-traits": "Character Traits",
    "reptiles": "Reptiles",
    "phonics": "Phonics",
    "beginning-letters": "Phonics",
    "digraphs": "Phonics",
    "spot-the-difference": "Spot the Difference",
    "flashcards": "Flashcards",
    "sliding-puzzle": "Sliding Puzzle",
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
        response.raise_for_status()
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
                previous_line = url  # Save for the next line's context

if __name__ == "__main__":
    main()
