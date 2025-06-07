import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os


def fetch_urls_from_sitemap(sitemap_url):
    try:
        res = requests.get(sitemap_url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, 'xml')
        return [loc.text.strip() for loc in soup.find_all("loc")]
    except Exception as e:
        print(f"Failed to fetch {sitemap_url} - {e}")
        return []


def classify_sitemap(sitemap_url):
    if "post-sitemap" in sitemap_url:
        return "posts_urls.txt"
    elif "wpdmpro" in sitemap_url:
        return "pdf_urls.txt"
    elif "category-sitemap" in sitemap_url:
        return "categories_urls.txt"
    elif "wpdmcategory" in sitemap_url:
        return "pdf_categories_urls.txt"
    elif "wpdmtag" in sitemap_url:
        return "tags_urls.txt"
    elif "page-sitemap" in sitemap_url:
        return "pages_urls.txt"
    else:
        return "other_urls.txt"


def main():
    main_sitemap = "https://www.kiddoworksheets.com/sitemap.xml"
    print(f"Fetching main sitemap: {main_sitemap}")

    # Step 1: Fetch all child sitemaps
    child_sitemaps = fetch_urls_from_sitemap(main_sitemap)
    print(f"Found {len(child_sitemaps)} child sitemaps.\n")

    # Step 2: Create a folder to store all lists
    os.makedirs("sitemap_links", exist_ok=True)

    for sitemap_url in child_sitemaps:
        category_file = classify_sitemap(sitemap_url)
        print(f"Processing: {sitemap_url} → {category_file}")

        urls = fetch_urls_from_sitemap(sitemap_url)
        print(f"  → Found {len(urls)} URLs\n")

        file_path = os.path.join("sitemap_links", category_file)
        with open(file_path, 'a', encoding='utf-8') as f:
            for url in urls:
                f.write(url + "\n")


if __name__ == "__main__":
    main()
