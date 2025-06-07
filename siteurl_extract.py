import requests
from bs4 import BeautifulSoup

def get_all_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = set()
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('http'):
            links.add(href)
        elif href.startswith('/'):
            # Ensure url ends without slash if needed
            full_url = url.rstrip('/') + href
            links.add(full_url)
    return links

url = 'https://www.worksheetfun.com/'
all_links = get_all_links(url)

# Save all links to a file
with open('worksheetfun_urls.txt', 'w') as file:
    for link in sorted(all_links):
        file.write(link + '\n')

print(f"Saved {len(all_links)} URLs to worksheetfun_urls.txt")
