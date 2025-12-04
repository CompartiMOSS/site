#!/usr/bin/env python3
"""
Verification script to ensure all entrevistas have correct image paths
"""

import os
import re
from pathlib import Path

def verify_entrevistas():
    """Verify all entrevista files have correct image paths"""
    content_dir = Path('/home/adiaz/github/site/content/entrevistas')
    images_dir = content_dir / 'images'
    
    md_files = sorted(content_dir.glob('*.md'))
    
    files_to_update = []
    verified_count = 0
    
    for md_file in md_files:
        if md_file.name == '_index.md':
            continue
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if image path is correct
        if 'image: "https://' in content:
            # Using placeholder image, skip
            verified_count += 1
            continue
        
        # Check if local image path
        image_match = re.search(r'image: ["\']([^"\']+)["\']', content)
        if image_match:
            image_path = image_match.group(1)
            
            # Check if file exists
            if image_path.startswith('./images/'):
                local_image = images_dir / image_path.replace('./images/', '')
                if local_image.exists():
                    verified_count += 1
                else:
                    files_to_update.append((md_file.name, image_path, "File not found"))
    
    print(f"✓ Verified: {verified_count} files")
    print(f"✗ Issues found: {len(files_to_update)}")
    
    if files_to_update:
        print("\nFiles needing updates:")
        for filename, image_path, reason in files_to_update:
            print(f"  - {filename}: {image_path} ({reason})")
    
    return len(files_to_update) == 0

if __name__ == '__main__':
    success = verify_entrevistas()
    exit(0 if success else 1)
