#!/usr/bin/env python3
"""
Script to add the first image URL from magazine articles to the frontmatter.
Processes all magazine numbers except numero-62.
"""

import os
import re
from pathlib import Path


def extract_number_from_folder(folder_name):
    """Extract the number from a folder name like 'numero-59' -> '59'"""
    match = re.match(r'numero-(\d+)', folder_name)
    return match.group(1) if match else None


def parse_frontmatter(content):
    """
    Parse the frontmatter from markdown content.
    Returns (frontmatter_dict, frontmatter_end_index)
    """
    if not content.startswith('---'):
        return {}, 0
    
    # Find the end of frontmatter
    end_match = re.search(r'\n---\n', content[3:])
    if not end_match:
        return {}, 0
    
    frontmatter_end = end_match.end() + 3
    frontmatter_content = content[3:frontmatter_end-4]
    
    # Parse frontmatter into dict
    frontmatter = {}
    for line in frontmatter_content.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip()
    
    return frontmatter, frontmatter_end


def find_first_image(content, frontmatter_end):
    """
    Find the first image URL in the markdown content after frontmatter.
    Returns the image path or None.
    """
    # Get content after frontmatter
    body = content[frontmatter_end:]
    
    # Pattern to match markdown images: ![alt text](image.png)
    image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    
    match = re.search(image_pattern, body)
    if match:
        return match.group(2)  # Return the image URL
    
    return None


def add_image_to_frontmatter(file_path):
    """
    Add the first image URL to the frontmatter if not already present.
    Returns True if file was modified, False otherwise.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse frontmatter
    frontmatter, frontmatter_end = parse_frontmatter(content)
    
    if frontmatter_end == 0:
        print(f"    ⚠️  {file_path.name}: No frontmatter found")
        return False
    
    # Check if image field already exists
    if 'image' in frontmatter and frontmatter['image'].strip().strip('"\''):
        return False  # Already has an image
    
    # Find first image in content
    first_image = find_first_image(content, frontmatter_end)
    
    if not first_image:
        return False  # No image found in content
    
    # Reconstruct frontmatter with image field
    frontmatter_lines = content[3:frontmatter_end-4].split('\n')
    
    # Find the position to insert the image field (after keywords or at the end)
    insert_position = len(frontmatter_lines)
    for i, line in enumerate(frontmatter_lines):
        if line.strip().startswith('keywords:') or line.strip().startswith('excerpt:'):
            insert_position = i + 1
            break
    
    # Insert the image field
    frontmatter_lines.insert(insert_position, f'image: "{first_image}"')
    
    # Reconstruct the file
    new_frontmatter = '---\n' + '\n'.join(frontmatter_lines) + '\n---\n'
    new_content = new_frontmatter + content[frontmatter_end:]
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True


def process_magazine_folder(folder_path, exclude_number='62'):
    """
    Process all markdown files in a magazine folder.
    
    Args:
        folder_path: Path to the magazine folder
        exclude_number: Magazine number to exclude (default: '62')
    
    Returns:
        Number of files modified
    """
    folder_name = os.path.basename(folder_path)
    magazine_number = extract_number_from_folder(folder_name)
    
    if not magazine_number:
        return 0
    
    # Skip the excluded number
    if magazine_number == exclude_number:
        print(f"⏭️  Skipping {folder_name} (excluded)")
        return 0
    
    files_modified = 0
    
    # Process all markdown files in the folder
    for md_file in Path(folder_path).glob('*.md'):
        # Skip _index.md files
        if md_file.name == '_index.md':
            continue
        
        try:
            if add_image_to_frontmatter(md_file):
                files_modified += 1
                print(f"  ✅ {md_file.name}: Image added to frontmatter")
        except Exception as e:
            print(f"  ❌ {md_file.name}: Error - {str(e)}")
    
    return files_modified


def main():
    """Main function to process all magazine folders."""
    # Get the content/revistas directory
    script_dir = Path(__file__).parent
    revistas_dir = script_dir / 'content' / 'revistas'
    
    if not revistas_dir.exists():
        print(f"❌ Error: Directory not found: {revistas_dir}")
        return
    
    print("🖼️  Adding first image to frontmatter for magazine articles...")
    print(f"📂 Processing directory: {revistas_dir}")
    print(f"⚠️  Excluding: numero-62\n")
    
    total_files = 0
    folders_processed = 0
    
    # Get all numero-* folders and sort them
    numero_folders = sorted([d for d in revistas_dir.iterdir() 
                           if d.is_dir() and d.name.startswith('numero-')])
    
    for folder in numero_folders:
        files_modified = process_magazine_folder(folder)
        if files_modified > 0 or folder.name != 'numero-62':
            folders_processed += 1
            total_files += files_modified
            if files_modified > 0:
                print(f"✨ {folder.name}: {files_modified} file(s) updated\n")
    
    print("\n" + "=" * 60)
    print("📊 Summary:")
    print(f"  Folders processed: {folders_processed}")
    print(f"  Files updated: {total_files}")
    print("=" * 60)
    
    if total_files > 0:
        print("\n✅ Frontmatter image fields successfully added!")
    else:
        print("\n✨ No changes needed - all files already have image fields or no images found!")


if __name__ == '__main__':
    main()
