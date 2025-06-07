import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.worksheetfun.com"
START_PAGE = BASE_URL
OUTPUT_FILE = "worksheetfun_urls.txt"

def get_links():
    response = requests.get(START_PAGE)
    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find_all("a", href=True)
    pdf_links = []

    for link in links:
        href = link['href']
        if ".pdf" in href or "/printable-" in href or "/worksheets/" in href:
            full_url = href if href.startswith("http") else BASE_URL + href
            pdf_links.append(full_url)

    return sorted(set(pdf_links))

def save_links(links):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for link in links:
            f.write(link + "\n")
    print(f"Saved {len(links)} worksheet links to {OUTPUT_FILE}")

if __name__ == "__main__":
    links = get_links()
    save_links(links)
