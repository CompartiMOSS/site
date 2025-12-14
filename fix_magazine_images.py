#!/usr/bin/env python3
"""
Script to fix image paths in magazine articles.
Converts: ../images/article-name/image.png
To: ../../../images/numeroX/article-name/image.png

Processes all magazine numbers except numero-62.
"""

import os
import re
from pathlib import Path


def extract_number_from_folder(folder_name):
    """Extract the number from a folder name like 'numero-59' -> '59'"""
    match = re.match(r'numero-(\d+)', folder_name)
    return match.group(1) if match else None


def fix_image_paths_in_file(file_path, magazine_number):
    """
    Fix image paths in a markdown file.
    
    Args:
        file_path: Path to the markdown file
        magazine_number: The magazine number (e.g., '59')
    
    Returns:
        Number of replacements made
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match incorrect paths with ../../../images/numeroX/ or more levels
    # This will match patterns like:
    # - ../../../images/numeroX/article-name/image.png
    # - ../../../../../images/numeroX/numeroX/article-name/image.png (duplicate)
    pattern = rf'\.\.(/\.\.)+/images/numero{magazine_number}(/numero{magazine_number})?/([^)"\s]+)'
    
    # Check if there are any matches to replace
    matches = re.findall(pattern, content)
    if not matches:
        return 0
    
    # Replace with the correct format: ../images/article-name/image.png
    replacement = r'../images/\3'
    new_content = re.sub(pattern, replacement, content)
    
    # Only write if content changed
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return len(matches)
    
    return 0


def process_magazine_folder(folder_path, exclude_number='62'):
    """
    Process all markdown files in a magazine folder.
    
    Args:
        folder_path: Path to the magazine folder (e.g., .../numero-59/)
        exclude_number: Magazine number to exclude (default: '62')
    
    Returns:
        Tuple of (files_processed, total_replacements)
    """
    folder_name = os.path.basename(folder_path)
    magazine_number = extract_number_from_folder(folder_name)
    
    if not magazine_number:
        return 0, 0
    
    # Skip the excluded number
    if magazine_number == exclude_number:
        print(f"⏭️  Skipping {folder_name} (excluded)")
        return 0, 0
    
    files_processed = 0
    total_replacements = 0
    
    # Process all markdown files in the folder
    for md_file in Path(folder_path).glob('*.md'):
        # Skip _index.md files
        if md_file.name == '_index.md':
            continue
        
        replacements = fix_image_paths_in_file(md_file, magazine_number)
        if replacements > 0:
            files_processed += 1
            total_replacements += replacements
            print(f"  ✅ {md_file.name}: {replacements} image(s) fixed")
    
    return files_processed, total_replacements


def main():
    """Main function to process all magazine folders."""
    # Get the content/revistas directory
    script_dir = Path(__file__).parent
    revistas_dir = script_dir / 'content' / 'revistas'
    
    if not revistas_dir.exists():
        print(f"❌ Error: Directory not found: {revistas_dir}")
        return
    
    print("🔧 Fixing image paths to correct format: ../images/article-name/image.png")
    print(f"📂 Processing directory: {revistas_dir}")
    print(f"⚠️  Excluding: numero-62\n")
    
    total_files = 0
    total_replacements = 0
    folders_processed = 0
    
    # Get all numero-* folders and sort them
    numero_folders = sorted([d for d in revistas_dir.iterdir() 
                           if d.is_dir() and d.name.startswith('numero-')])
    
    for folder in numero_folders:
        files, replacements = process_magazine_folder(folder)
        if files > 0 or folder.name != 'numero-62':
            folders_processed += 1
            total_files += files
            total_replacements += replacements
            if files > 0:
                print(f"✨ {folder.name}: {files} file(s) updated, {replacements} image(s) fixed\n")
    
    print("\n" + "=" * 60)
    print("📊 Summary:")
    print(f"  Folders processed: {folders_processed}")
    print(f"  Files updated: {total_files}")
    print(f"  Total image paths fixed: {total_replacements}")
    print("=" * 60)
    
    if total_replacements > 0:
        print("\n✅ Image paths successfully updated!")
    else:
        print("\n✨ No changes needed - all paths are already correct!")


if __name__ == '__main__':
    main()
