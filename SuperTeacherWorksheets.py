import requests
from bs4 import BeautifulSoup

SITEMAP_URL = "https://www.superteacherworksheets.com/sitemap.xml"
OUTPUT_FILE = "superteacher_urls.txt"

def fetch_sitemap_links():
    response = requests.get(SITEMAP_URL)
    soup = BeautifulSoup(response.content, "xml")  # Proper XML parser
    urls = soup.find_all("loc")
    worksheet_links = []

    for tag in urls:
        url = tag.text.strip()
        # Filter for pages that likely contain worksheets
        if any(kw in url for kw in [
            "/addition", "/subtraction", "/multiplication", "/division",
            "/phonics", "/reading", "/grammar", "/math", "/index", "/puzzles"
        ]):
            worksheet_links.append(url)

    return sorted(set(worksheet_links))

def save_links(links):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for link in links:
            f.write(link + "\n")
    print(f"✓ Saved {len(links)} worksheet links to {OUTPUT_FILE}")

if __name__ == "__main__":
    links = fetch_sitemap_links()
    save_links(links)
