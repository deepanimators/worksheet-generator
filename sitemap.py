import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_sitemap_urls(base_url):
    sitemap_url = urljoin(base_url, '/sitemap.xml')
    print(f"Fetching sitemap: {sitemap_url}")

    try:
        response = requests.get(sitemap_url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to retrieve sitemap: {e}")
        return []

    soup = BeautifulSoup(response.content, 'xml')
    urls = [loc.text.strip() for loc in soup.find_all("loc")]
    print(f"Found {len(urls)} URLs in sitemap.")

    return urls

def main():
    base_url = "https://www.kiddoworksheets.com"
    sitemap_urls = fetch_sitemap_urls(base_url)

    for i, url in enumerate(sitemap_urls, start=1):
        print(f"{i}. {url}")

    # Optional: Save to file
    with open("kiddoworksheets_sitemap_urls.txt", "w", encoding="utf-8") as f:
        for url in sitemap_urls:
            f.write(url + "\n")

if __name__ == "__main__":
    main()
