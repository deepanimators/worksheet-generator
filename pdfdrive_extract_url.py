import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

visited = set()
pdfdrive_links = set()

BASE_URL = "https://pdfdrive.com.co"
MAX_DEPTH = 10  # Avoid infinite crawling
MAX_PAGES = 100000  # Adjust depending on how deep you want to go

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36"
}

def is_internal(url):
    return url.startswith(BASE_URL) or url.startswith("/")

def normalize_url(url, base):
    return urljoin(base, url)

def crawl(url, depth=0):
    if url in visited or depth > MAX_DEPTH or len(visited) > MAX_PAGES:
        return
    try:
        response = requests.get(url, headers=headers, timeout=10)
        visited.add(url)
        print(f"[{len(visited)}] Crawling: {url} (depth {depth})")

        if response.status_code != 200:
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        for link_tag in soup.find_all("a", href=True):
            link = link_tag['href']
            full_url = normalize_url(link, BASE_URL)
            if is_internal(full_url) and "pdf" in full_url.lower():  # optional: refine
                pdfdrive_links.add(full_url)
            if is_internal(full_url) and full_url not in visited:
                crawl(full_url, depth + 1)

        time.sleep(0.5)  # Be polite and avoid hammering the server
    except Exception as e:
        print(f"⚠️ Failed: {url} | {e}")

if __name__ == "__main__":
    crawl(BASE_URL)

    with open("pdfdrive_all_urls.txt", "w", encoding="utf-8") as f:
        for link in sorted(pdfdrive_links):
            f.write(link + "\n")

    print(f"\n✅ Crawled {len(visited)} pages and found {len(pdfdrive_links)} PDF-related URLs.")
