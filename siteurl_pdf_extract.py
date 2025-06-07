import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

BASE_URL = 'https://www.worksheetfun.com/'
visited = set()
pdf_links = set()


def is_valid_url(url):
    # Only stay within the same domain
    parsed = urlparse(url)
    return parsed.netloc == urlparse(BASE_URL).netloc


def crawl(url):
    if url in visited:
        return
    visited.add(url)
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link['href'].strip()

            # Get absolute URL
            full_url = urljoin(url, href)

            if full_url.endswith('.pdf'):
                pdf_links.add(full_url)
            elif is_valid_url(full_url) and full_url not in visited:
                crawl(full_url)

        # Be polite and don't overload the server
        time.sleep(0.5)
    except Exception as e:
        print(f"Failed to crawl {url}: {e}")


crawl(BASE_URL)

# Save PDF links to file
with open('worksheetfun_pdf_urls.txt', 'w') as f:
    for pdf in sorted(pdf_links):
        f.write(pdf + '\n')

print(f"Found and saved {len(pdf_links)} PDF URLs.")
