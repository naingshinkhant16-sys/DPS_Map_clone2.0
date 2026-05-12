import re
import os
import requests
from urllib.parse import urljoin, urlparse

css_file = '/home/ubuntu/dpsmap_clone/assets/index-BdgmOU_-.css'
base_url = 'https://dpsmap.com/assets/' # Assets are usually relative to the CSS location
output_dir = '/home/ubuntu/dpsmap_clone/assets'

with open(css_file, 'r') as f:
    content = f.read()

# Find all url(...) patterns
urls = re.findall(r"url\(['\"]?([^'\"\)]+)['\"]?\)", content)
unique_urls = list(set(urls))

print(f"Found {len(unique_urls)} URLs in CSS.")

for url in unique_urls:
    if url.startswith('data:'):
        continue
    
    # Resolve URL
    full_url = urljoin(base_url, url)
    print(f"Downloading {full_url}...")
    
    try:
        response = requests.get(full_url, timeout=10)
        if response.status_code == 200:
            # We want to keep the relative path structure if possible, 
            # but for simplicity we'll flatten it or match the CSS reference.
            filename = os.path.basename(urlparse(url).path)
            filepath = os.path.join(output_dir, filename)
            
            # Ensure subdirectories exist if needed (though we're flattening here)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            # Update the CSS content to point to the local file
            content = content.replace(url, filename)
    except Exception as e:
        print(f"Error: {e}")

# Save the updated CSS
with open(css_file, 'w') as f:
    f.write(content)

print("CSS asset extraction complete.")
