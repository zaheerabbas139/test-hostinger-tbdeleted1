#!/usr/bin/env python3
"""
Downloads media attachments cataloged in scripts/media-manifest.json into public/assets/images/.
"""

import os
import json
import urllib.request
import urllib.error

MANIFEST_FILE = 'scripts/media-manifest.json'
TARGET_DIR = 'public/assets/images'

def main():
    if not os.path.exists(MANIFEST_FILE):
        print(f"Manifest {MANIFEST_FILE} not found.")
        return

    os.makedirs(TARGET_DIR, exist_ok=True)

    with open(MANIFEST_FILE, 'r') as f:
        manifest = json.load(f)

    print(f"Total media items in manifest: {len(manifest)}")
    downloaded = 0
    skipped = 0
    failed = 0

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    for item_id, data in manifest.items():
        url = data.get('url', '')
        filename = data.get('filename', '')

        # Check if valid image filename
        if not filename or not any(filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.webp', '.svg', '.gif']):
            skipped += 1
            continue

        target_path = os.path.join(TARGET_DIR, filename)
        if os.path.exists(target_path) and os.path.getsize(target_path) > 0:
            print(f"[EXISTS] {filename}")
            downloaded += 1
            continue

        try:
            print(f"[DOWNLOADING] {url} -> {target_path}")
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response, open(target_path, 'wb') as out_file:
                out_file.write(response.read())
            downloaded += 1
        except Exception as e:
            print(f"[FAILED] {url}: {e}")
            failed += 1

    print(f"\nDownload Summary: {downloaded} downloaded/present, {skipped} skipped, {failed} failed.")

if __name__ == '__main__':
    main()

