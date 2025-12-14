#!/usr/bin/env python3
"""
Script to sync podcast episodes from RSS feed to podcast.yaml
"""

import xml.etree.ElementTree as ET
import yaml
import requests
from datetime import datetime
import re
from html import unescape

RSS_URL = "https://feeds.ivoox.com/feed_fg_f11376815_filtro_1.xml"
YAML_FILE = "data/podcast.yaml"

def clean_text(text):
    """Remove HTML tags and clean text"""
    if not text:
        return ""
    # Remove CDATA
    text = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', text, flags=re.DOTALL)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Unescape HTML entities
    text = unescape(text)
    # Clean extra whitespace
    text = ' '.join(text.split())
    return text.strip()

def parse_duration(duration_str):
    """Convert duration string to HH:MM:SS format"""
    if not duration_str:
        return "00:00"
    
    parts = duration_str.split(':')
    if len(parts) == 3:
        return duration_str
    elif len(parts) == 2:
        return duration_str
    else:
        return "00:00"

def parse_date(date_str):
    """Convert RFC 822 date to Spanish format"""
    try:
        # Parse the RFC 822 date
        dt = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
        
        # Spanish month names
        months_es = {
            1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
            5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
            9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
        }
        
        return f"{dt.day} de {months_es[dt.month]} de {dt.year}"
    except:
        return date_str

def create_slug(title):
    """Create a URL-friendly slug from title"""
    # Remove "Unplugged XXX:" prefix and clean
    title = re.sub(r'^Unplugged \d+:\s*', '', title, flags=re.IGNORECASE)
    title = re.sub(r'^Unnplugged \d+:\s*', '', title, flags=re.IGNORECASE)
    
    # Convert to lowercase and replace spaces/special chars
    slug = title.lower()
    slug = re.sub(r'[áàäâ]', 'a', slug)
    slug = re.sub(r'[éèëê]', 'e', slug)
    slug = re.sub(r'[íìïî]', 'i', slug)
    slug = re.sub(r'[óòöô]', 'o', slug)
    slug = re.sub(r'[úùüû]', 'u', slug)
    slug = re.sub(r'[ñ]', 'n', slug)
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    slug = slug.strip('-')
    
    return slug[:100]  # Limit length

def extract_episode_number(title):
    """Extract episode number from title"""
    match = re.search(r'Unplugged\s+(\d+)', title, re.IGNORECASE)
    if match:
        return int(match.group(1))
    match = re.search(r'Unnplugged\s+(\d+)', title, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None

def fetch_rss_episodes():
    """Fetch and parse episodes from RSS feed"""
    print(f"Fetching RSS feed from {RSS_URL}...")
    response = requests.get(RSS_URL)
    response.raise_for_status()
    
    root = ET.fromstring(response.content)
    
    # Define namespaces
    namespaces = {
        'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
    }
    
    episodes = []
    
    for item in root.findall('.//item'):
        title = clean_text(item.findtext('title', ''))
        
        # Extract episode number
        episode_num = extract_episode_number(title)
        if not episode_num:
            continue
        
        # Get enclosure URL (audio file)
        enclosure = item.find('enclosure')
        audio_url = enclosure.get('url') if enclosure is not None else ""
        
        # Get description
        description = clean_text(item.findtext('description', ''))
        # Limit description length
        if len(description) > 200:
            description = description[:197] + '...'
        
        # Get date
        pub_date = item.findtext('pubDate', '')
        formatted_date = parse_date(pub_date)
        
        # Get duration
        duration = item.findtext('{http://www.itunes.com/dtds/podcast-1.0.dtd}duration', '')
        formatted_duration = parse_duration(duration)
        
        # Create slug
        slug = f"unplugged-{episode_num}-{create_slug(title)}"
        
        episode = {
            'id': str(episode_num),
            'slug': slug,
            'title': title,
            'description': description,
            'date': formatted_date,
            'duration': formatted_duration,
            'audioUrl': audio_url
        }
        
        episodes.append(episode)
    
    print(f"Found {len(episodes)} episodes in RSS feed")
    return episodes

def load_existing_episodes():
    """Load existing episodes from YAML file"""
    try:
        with open(YAML_FILE, 'r', encoding='utf-8') as f:
            episodes = yaml.safe_load(f) or []
        print(f"Loaded {len(episodes)} existing episodes from {YAML_FILE}")
        return episodes
    except FileNotFoundError:
        print(f"{YAML_FILE} not found, starting fresh")
        return []

def merge_episodes(existing, new_episodes):
    """Merge new episodes with existing ones"""
    # Create a dict of existing episodes by ID
    existing_dict = {ep['id']: ep for ep in existing}
    
    # Merge new episodes
    for episode in new_episodes:
        if episode['id'] not in existing_dict:
            existing_dict[episode['id']] = episode
            print(f"Adding episode {episode['id']}: {episode['title']}")
        else:
            # Update existing episode with new data
            existing_dict[episode['id']].update(episode)
            print(f"Updating episode {episode['id']}: {episode['title']}")
    
    # Convert back to list and sort by ID (descending)
    merged = list(existing_dict.values())
    merged.sort(key=lambda x: int(x['id']), reverse=True)
    
    return merged

def save_episodes(episodes):
    """Save episodes to YAML file"""
    with open(YAML_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(episodes, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    print(f"Saved {len(episodes)} episodes to {YAML_FILE}")

def main():
    try:
        # Fetch episodes from RSS
        rss_episodes = fetch_rss_episodes()
        
        # Load existing episodes
        existing_episodes = load_existing_episodes()
        
        # Merge episodes
        merged_episodes = merge_episodes(existing_episodes, rss_episodes)
        
        # Save to file
        save_episodes(merged_episodes)
        
        print("\n✅ Podcast sync completed successfully!")
        print(f"Total episodes: {len(merged_episodes)}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
