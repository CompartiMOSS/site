#!/usr/bin/env python3
"""
Migration script to convert author MDX files from migration/autores to content/autores MD format.
Transforms Gatsby MDX format to Hugo MD format.
"""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, Optional


def extract_frontmatter(content: str) -> tuple[Optional[Dict], str]:
    """Extract YAML frontmatter from MDX file."""
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)
    
    if match:
        try:
            frontmatter = yaml.safe_load(match.group(1))
            body = match.group(2).strip()
            return frontmatter, body
        except yaml.YAMLError as e:
            print(f"Error parsing YAML: {e}")
            return None, content
    return None, content


def extract_twitter_handle(twitter_url: str) -> str:
    """Extract Twitter handle from URL."""
    if not twitter_url:
        return ""
    # Remove trailing slashes and extract the last part
    twitter_url = twitter_url.rstrip('/')
    handle = twitter_url.split('/')[-1]
    # Remove @ if present
    return handle.lstrip('@')


def transform_photo_path(photo_path: str, author_id: str) -> str:
    """Transform photo path from Gatsby to Hugo format."""
    if not photo_path:
        return ""
    
    # Extract filename from path
    filename = os.path.basename(photo_path)
    
    # If filename is the author_id.png, use it; otherwise try to infer
    if not filename or filename == "":
        return f"./images/{author_id}.png"
    
    return f"./images/{filename}"


def convert_mdx_to_md(mdx_content: str, filename: str) -> Optional[str]:
    """Convert MDX author file to MD format."""
    frontmatter, body = extract_frontmatter(mdx_content)
    
    if not frontmatter:
        print(f"No frontmatter found in {filename}")
        return None
    
    # Extract fields from MDX frontmatter
    author_id = frontmatter.get('id', '')
    title = frontmatter.get('title', '')
    job_title = frontmatter.get('jobTitle', '')
    photo = frontmatter.get('photo', '')
    twitter_url = frontmatter.get('twitter', '')
    blog = frontmatter.get('blog', '')
    content = frontmatter.get('content', '')
    
    # Transform data
    twitter_handle = extract_twitter_handle(twitter_url)
    avatar_path = transform_photo_path(photo, author_id)
    
    # Clean content - remove extra whitespace and normalize
    bio = content.strip() if content else ''
    
    # Build new MD frontmatter
    new_frontmatter = {
        'title': title,
        'bio': bio,
        'avatar': avatar_path,
        'role': job_title,
    }
    
    # Add optional fields if they exist
    if twitter_handle:
        new_frontmatter['twitter'] = f"@{twitter_handle}" if not twitter_handle.startswith('@') else twitter_handle
    
    if blog:
        new_frontmatter['linkedin'] = ""  # LinkedIn not in source, leave empty
    
    # Generate MD content
    md_content = "---\n"
    md_content += yaml.dump(new_frontmatter, allow_unicode=True, sort_keys=False, default_flow_style=False)
    md_content += "---\n"
    
    return md_content


def migrate_authors(source_dir: str, target_dir: str, dry_run: bool = True):
    """Migrate all author MDX files to MD format."""
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    
    if not source_path.exists():
        print(f"Error: Source directory {source_dir} does not exist")
        return
    
    if not target_path.exists():
        if not dry_run:
            target_path.mkdir(parents=True, exist_ok=True)
            print(f"Created target directory: {target_dir}")
        else:
            print(f"Would create target directory: {target_dir}")
    
    # Process all MDX files
    mdx_files = list(source_path.glob("*.mdx"))
    
    # Skip index.mdx
    mdx_files = [f for f in mdx_files if f.name != 'index.mdx']
    
    print(f"\nFound {len(mdx_files)} author files to migrate\n")
    
    success_count = 0
    error_count = 0
    
    for mdx_file in sorted(mdx_files):
        try:
            print(f"Processing: {mdx_file.name}")
            
            # Read MDX file
            with open(mdx_file, 'r', encoding='utf-8') as f:
                mdx_content = f.read()
            
            # Convert to MD
            md_content = convert_mdx_to_md(mdx_content, mdx_file.name)
            
            if not md_content:
                print(f"  ❌ Failed to convert {mdx_file.name}")
                error_count += 1
                continue
            
            # Generate output filename (replace .mdx with .md)
            output_filename = mdx_file.stem + '.md'
            output_path = target_path / output_filename
            
            if dry_run:
                print(f"  ✓ Would create: {output_path}")
                print(f"  Preview (first 300 chars):")
                print(f"  {md_content[:300]}...")
            else:
                # Write MD file
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(md_content)
                print(f"  ✓ Created: {output_path}")
            
            success_count += 1
            
        except Exception as e:
            print(f"  ❌ Error processing {mdx_file.name}: {e}")
            error_count += 1
    
    print(f"\n{'='*60}")
    print(f"Migration Summary:")
    print(f"  Total files: {len(mdx_files)}")
    print(f"  Successful: {success_count}")
    print(f"  Errors: {error_count}")
    print(f"  Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print(f"{'='*60}\n")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Migrate author MDX files to MD format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run (preview changes)
  python migrate_autores.py --dry-run

  # Actually perform the migration
  python migrate_autores.py

  # Custom source and target directories
  python migrate_autores.py --source /path/to/migration/autores --target /path/to/content/autores
        """
    )
    
    parser.add_argument(
        '--source',
        default='migration/autores',
        help='Source directory containing MDX files (default: migration/autores)'
    )
    
    parser.add_argument(
        '--target',
        default='content/autores',
        help='Target directory for MD files (default: content/autores)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without writing files'
    )
    
    args = parser.parse_args()
    
    print("Author MDX to MD Migration Script")
    print("=" * 60)
    print(f"Source: {args.source}")
    print(f"Target: {args.target}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print("=" * 60)
    
    migrate_authors(args.source, args.target, args.dry_run)
    
    if args.dry_run:
        print("\n💡 This was a dry run. Use without --dry-run to perform actual migration.")


if __name__ == '__main__':
    main()
