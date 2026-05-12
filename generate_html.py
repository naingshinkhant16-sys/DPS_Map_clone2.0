from bs4 import BeautifulSoup
import json
import os

html_file = '/home/ubuntu/browser_html/dpsmap_com_page_1778595784172.html'
mapping_file = '/home/ubuntu/asset_mapping.json'
output_file = '/home/ubuntu/dpsmap_clone/index.html'

with open(mapping_file, 'r') as f:
    mapping = json.load(f)

with open(html_file, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

# Update image sources
for img in soup.find_all('img'):
    src = img.get('src')
    if src:
        # Resolve relative URLs to absolute first for matching
        from urllib.parse import urljoin
        abs_src = urljoin('https://dpsmap.com/', src)
        if abs_src in mapping:
            img['src'] = mapping[abs_src]

# Update CSS links
for link in soup.find_all('link', rel='stylesheet'):
    href = link.get('href')
    if href:
        abs_href = urljoin('https://dpsmap.com/', href)
        if abs_href in mapping:
            link['href'] = mapping[abs_href]

# Update JS scripts
for script in soup.find_all('script'):
    src = script.get('src')
    if src:
        abs_src = urljoin('https://dpsmap.com/', src)
        if abs_src in mapping:
            script['src'] = mapping[abs_src]
    # Remove tracking scripts
    elif script.string and ('gtag' in script.string or 'fbq' in script.string):
        script.decompose()

# Clean up some common tracking or external widgets if needed
# (Optional: JotForm, Chatbots, etc.)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(soup.prettify())

print(f"Generated {output_file}")
