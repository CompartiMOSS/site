#!/usr/bin/env python3
"""
Migration script to convert entrevistas from old MDX format to new MD format
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime

def parse_old_format(file_path):
    """Parse old MDX format entrevista file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not frontmatter_match:
        return None
    
    frontmatter_text = frontmatter_match.group(1)
    body = content[frontmatter_match.end():].strip()
    
    # Parse frontmatter fields
    frontmatter = {}
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip("'\"[]")
            frontmatter[key] = value
    
    return {
        'frontmatter': frontmatter,
        'body': body
    }

def convert_to_new_format(parsed_data, image_path=None):
    """Convert parsed data to new format"""
    fm = parsed_data['frontmatter']
    body = parsed_data['body']
    
    # Extract name from author or title
    author = fm.get('author', '')
    title = fm.get('title', '')
    
    # Extract name from title if it's "Entrevista a ..."
    name = title.replace('Entrevista a ', '').replace('Entrevista MVP: ', '').strip()
    if not name:
        name = author
    
    # Parse date - old format is DD/MM/YYYY
    date_str = fm.get('date', '')
    try:
        if '/' in date_str:
            date_parts = date_str.split('/')
            if len(date_parts) == 3:
                date_obj = datetime(int(date_parts[2]), int(date_parts[1]), int(date_parts[0]))
                date_str = date_obj.isoformat()
    except:
        date_str = datetime.now().isoformat()
    
    # Create slug from filename
    slug = fm.get('slug', '').split('/')[-1]
    if not slug:
        slug = name.lower().replace(' ', '-')
    
    # Use local image if provided, otherwise use placeholder
    if image_path and os.path.exists(image_path):
        image = f"./images/{os.path.basename(image_path)}"
    else:
        image = "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=800&q=80"
    
    # Clean up body - remove author image markdown
    body = re.sub(r'!\[.*?\]\([^)]*#author\)', '', body)
    body = body.strip()
    
    # Create new frontmatter
    new_frontmatter = f'''---
title: "Entrevista: {name}"
date: {date_str}
name: "{name}"
excerpt: "{name} comparte su experiencia y visión sobre la tecnología Microsoft."
image: "{image}"
---

'''
    
    return new_frontmatter + body

def migrate_files():
    """Main migration function"""
    migration_dir = Path('/home/adiaz/github/site/migration/entrevistas')
    content_dir = Path('/home/adiaz/github/site/content/entrevistas')
    migration_images = migration_dir / 'images'
    content_images = content_dir / 'images'
    
    # Create images directory if it doesn't exist
    content_images.mkdir(parents=True, exist_ok=True)
    
    # Get all MDX files
    mdx_files = sorted(migration_dir.glob('*.mdx'))
    
    migrated_count = 0
    failed_count = 0
    skipped_count = 0
    
    for mdx_file in mdx_files:
        try:
            # Skip if already migrated (file with same name exists in .md)
            md_file = content_dir / f"{mdx_file.stem}.md"
            if md_file.exists():
                print(f"⊘ SKIPPED: {mdx_file.name} (already exists)")
                skipped_count += 1
                continue
            
            # Parse old format
            parsed = parse_old_format(mdx_file)
            if not parsed:
                print(f"✗ FAILED: {mdx_file.name} (couldn't parse)")
                failed_count += 1
                continue
            
            # Find corresponding image
            image_path = None
            base_name = mdx_file.stem
            author_id = parsed['frontmatter'].get('authorId', '').lower()
            
            # Try different image name patterns
            for img_pattern in [f"{base_name}.png", f"{author_id}.png"]:
                potential_image = migration_images / img_pattern
                if potential_image.exists():
                    image_path = potential_image
                    break
            
            # Convert to new format
            new_content = convert_to_new_format(parsed, image_path)
            
            # Write new file
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            # Copy image if found
            if image_path and image_path.exists():
                dest_image = content_images / image_path.name
                if not dest_image.exists():
                    shutil.copy2(image_path, dest_image)
            
            print(f"✓ MIGRATED: {mdx_file.name} → {md_file.name}")
            migrated_count += 1
            
        except Exception as e:
            print(f"✗ ERROR: {mdx_file.name} - {str(e)}")
            failed_count += 1
    
    print(f"\n{'='*60}")
    print(f"Migration Summary:")
    print(f"  Migrated:  {migrated_count}")
    print(f"  Skipped:   {skipped_count}")
    print(f"  Failed:    {failed_count}")
    print(f"  Total:     {len(mdx_files)}")

if __name__ == '__main__':
    migrate_files()
