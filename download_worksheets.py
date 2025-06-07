import os
import requests
from urllib.parse import urlparse

def download_and_categorize_pdfs(url_file_path, base_download_dir="Downloaded_Worksheets"):
    categories = {
        "Addition": ["addition", "add", "sum"],
        "Subtraction": ["subtraction", "subtract", "minus"],
        "Multiplication": ["multiplication", "multiply", "mult", "times-table"],
        "Division": ["division", "divide", "quotient"],
        "Phonics": ["phonics", "digraph", "long-vowel", "beginning-letters"],
        "Grammar": ["grammar", "nouns", "verbs", "adjectives", "prepositions", "homophones", "conjunctions"],
        "Reading Comprehension": ["reading", "comprehension", "story", "passage"],
        "Word Search": ["word-search", "wordsearch"],
        "Coloring": ["coloring", "color", "fill-the-color", "color-by-number"],
        "Mystery Pictures": ["mystery-picture", "mystery"],
        "Math Riddles": ["math-riddle", "riddle"],
        "Flashcards": ["flashcard"],
        "Task Cards": ["task-card", "taskcard"],
        "Cut and Glue": ["cut-glue", "cutandglue"],
        "Daily Math Review": ["daily-math", "dailymath"],
        "Puzzles": ["puzzle", "shadow-match", "spot-the-difference"],
        "Buzz Series": ["buzz"],
        "Money Math": ["money", "coins", "currency"],
        "Crossword": ["crossword"],
        "Awards": ["award", "certificate"],
        "Decimals": ["decimal"],
        "Fractions": ["fraction"],
        "Telling Time": ["telling-time", "clock", "match-the-clock"],
        "Tracing Lines": ["tracing-lines"],
        "Handwriting Practice": ["handwriting"],
        "Cursive Writing": ["cursive"],
        "Matching Words to Pictures": ["matching-words", "word-to-picture"],
        "Body Parts": ["body-parts", "label-body"],
        "Counting": ["counting", "count", "tally"],
        "Opposite Words": ["opposite"],
        "Spelling Words": ["spelling"],
        "Others": []
    }

    os.makedirs(base_download_dir, exist_ok=True)
    for category in categories:
        os.makedirs(os.path.join(base_download_dir, category), exist_ok=True)

    failed_urls = []

    try:
        with open(url_file_path, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ File not found: {url_file_path}")
        return

    for url in urls:
        try:
            parsed = urlparse(url)
            filename = os.path.basename(parsed.path)
            if not filename.lower().endswith('.pdf'):
                print(f"⏩ Skipping non-PDF: {url}")
                continue

            filename_lower = filename.lower()
            target_category = "Others"
            for category, keywords in categories.items():
                if any(keyword in filename_lower for keyword in keywords):
                    target_category = category
                    break

            folder_path = os.path.join(base_download_dir, target_category)
            base_name, ext = os.path.splitext(filename)
            final_name = filename
            counter = 1
            while os.path.exists(os.path.join(folder_path, final_name)):
                final_name = f"{base_name}_{counter}{ext}"
                counter += 1

            final_path = os.path.join(folder_path, final_name)
            print(f"⬇️  Downloading {filename} → {target_category}")

            success = False
            for attempt in range(3):  # Retry up to 3 times
                try:
                    response = requests.get(url, stream=True, timeout=10)
                    response.raise_for_status()
                    with open(final_path, 'wb') as f:
                        for chunk in response.iter_content(8192):
                            f.write(chunk)
                    print(f"✅ Saved: {final_path}")
                    success = True
                    break
                except Exception as e:
                    print(f"⚠️  Attempt {attempt + 1} failed for {url}: {e}")

            if not success:
                failed_urls.append(url)

        except Exception as ex:
            print(f"❌ Error processing {url}: {ex}")
            failed_urls.append(url)

    if failed_urls:
        fail_log_path = os.path.join(base_download_dir, "failed_downloads.txt")
        with open(fail_log_path, "w", encoding="utf-8") as f:
            for url in failed_urls:
                f.write(url + "\n")
        print(f"\n❗ {len(failed_urls)} downloads failed. See: {fail_log_path}")
    else:
        print("\n🎉 All downloads completed successfully!")

if __name__ == "__main__":
    download_and_categorize_pdfs("worksheetfun_pdf_urls.txt")
