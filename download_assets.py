import json
import os
import requests
from urllib.parse import urlparse

with open('/home/ubuntu/assets.json', 'r') as f:
    assets = json.load(f)

output_dir = '/home/ubuntu/dpsmap_clone'
assets_dir = os.path.join(output_dir, 'assets')

if not os.path.exists(assets_dir):
    os.makedirs(assets_dir)

def download_file(url, folder):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            filename = os.path.basename(urlparse(url).path)
            if not filename:
                return None
            filepath = os.path.join(folder, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return filename
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return None

# Download CSS and JS to assets folder
# For the sake of a clean clone, we'll keep them in 'assets'
mapping = {}

for category in ['css', 'js', 'images']:
    for url in assets[category]:
        # Skip external trackers for now to keep it clean
        if 'facebook.net' in url or 'google-analytics' in url or 'statcounter' in url:
            continue
        filename = download_file(url, assets_dir)
        if filename:
            mapping[url] = f"assets/{filename}"

with open('/home/ubuntu/asset_mapping.json', 'w') as f:
    json.dump(mapping, f, indent=4)

print("Download complete.")
