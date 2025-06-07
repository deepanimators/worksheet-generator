import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_DOMAIN = "https://www.123homeschool4me.com"
SITEMAP_INDEX_URL = BASE_DOMAIN + "/sitemap_index.xml"  # Common Yoast format
OUTPUT_FILE = "123homeschool_urls.txt"

def get_sitemap_urls(index_url):
    response = requests.get(index_url)
    soup = BeautifulSoup(response.content, "xml")
    sitemap_tags = soup.find_all("loc")
    return [tag.text for tag in sitemap_tags if tag.text.endswith(".xml")]

def extract_links_from_sitemap(sitemap_url):
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.content, "xml")
    loc_tags = soup.find_all("loc")
    return [tag.text for tag in loc_tags]

def extract_pdf_links_from_page(page_url):
    try:
        response = requests.get(page_url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.find_all("a", href=True)
        pdf_links = []
        for link in links:
            href = link['href']
            if ".pdf" in href:
                full_url = href if href.startswith("http") else urljoin(BASE_DOMAIN, href)
                pdf_links.append(full_url)
        return pdf_links
    except Exception as e:
        print(f"✘ Failed to fetch page {page_url}: {e}")
        return []

def main():
    all_pdf_links = set()
    sitemap_urls = get_sitemap_urls(SITEMAP_INDEX_URL)

    for sitemap in sitemap_urls:
        print(f"📄 Reading sitemap: {sitemap}")
        page_urls = extract_links_from_sitemap(sitemap)
        for page in page_urls:
            print(f"🔍 Scanning page: {page}")
            pdfs = extract_pdf_links_from_page(page)
            all_pdf_links.update(pdfs)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for url in sorted(all_pdf_links):
            f.write(url + "\n")

    print(f"\n✅ Saved {len(all_pdf_links)} PDF worksheet links to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
