from bs4 import BeautifulSoup
import os
import requests
from urllib.parse import urljoin, urlparse

html_file = '/home/ubuntu/browser_html/dpsmap_com_page_1778595784172.html'
base_url = 'https://dpsmap.com/'
output_dir = '/home/ubuntu/dpsmap_clone'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(html_file, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

# Find all images, links to CSS, and scripts
assets = {
    'images': [],
    'css': [],
    'js': []
}

for img in soup.find_all('img'):
    src = img.get('src')
    if src:
        assets['images'].append(urljoin(base_url, src))

for link in soup.find_all('link', rel='stylesheet'):
    href = link.get('href')
    if href:
        assets['css'].append(urljoin(base_url, href))

for script in soup.find_all('script'):
    src = script.get('src')
    if src:
        assets['js'].append(urljoin(base_url, src))

# Also look for background images in style tags or inline styles
# (Simplified for now, will refine if needed)

print("Assets found:")
for key, value in assets.items():
    print(f"{key}: {len(value)}")
    for item in value[:5]: # Print first 5 of each
        print(f"  - {item}")

# Save the asset list to a file
import json
with open('/home/ubuntu/assets.json', 'w') as f:
    json.dump(assets, f, indent=4)
