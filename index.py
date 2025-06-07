import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from time import sleep

BASE_URL = "https://www.kiddoworksheets.com/"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get_soup(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        return BeautifulSoup(res.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"[Error] Could not fetch {url}: {e}")
        return None


def get_categories():
    soup = get_soup(BASE_URL)
    categories = {}
    for link in soup.select("ul.dropdown-menu li a"):
        name = link.text.strip()
        url = link['href']
        if 'worksheet' in url:
            categories[name] = url
    return categories


def get_worksheet_links(category_url):
    links = []
    page = 1

    while True:
        paginated_url = f"{category_url.rstrip('/')}/page/{page}/"
        soup = get_soup(paginated_url)

        if soup is None:
            break

        new_links = [a['href'] for a in soup.select(".entry-title a")]

        if not new_links:
            break  # Stop if no new links found

        links.extend(new_links)
        page += 1
        sleep(0.5)  # Be gentle to the server

    return list(set(links))  # Avoid duplicates


def get_download_link(worksheet_url):
    soup = get_soup(worksheet_url)
    if soup:
        button = soup.select_one("a.btn-download")
        if button and 'href' in button.attrs:
            return button['href']
    return None

def download_pdf(url, folder, filename):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        print(f"Already exists: {path}")
        return
    ...

def main():
    print("Fetching categories...")
    categories = get_categories()

    for category, url in categories.items():
        print(f"\nCategory: {category}")
        worksheet_links = get_worksheet_links(url)
        print(f"  Found {len(worksheet_links)} worksheets")

        for link in worksheet_links:
            title = link.rstrip('/').split('/')[-1].replace('-', '_')
            download_url = get_download_link(link)
            if download_url:
                download_pdf(download_url, f"Worksheets/{category}", f"{title}.pdf")
            sleep(0.3)

if __name__ == "__main__":
    main()
