#!/usr/bin/env python3
"""
Add additional entity types:
- URLs
- IPv6 addresses
- International phone numbers
- Emojis
- Social media usernames (Instagram, Facebook, LinkedIn, Telegram, Discord, Slack, WhatsApp)
- Social media URLs
- GeoJSON coordinates
- DMS coordinates
- Custom coordinate formats
"""

import json
import re
import random
from pathlib import Path
from typing import List, Dict

# Patterns
URL_PATTERN = re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+')
IPV6_PATTERN = re.compile(r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b|\b::1\b|\bfe80::[0-9a-fA-F:]+')
EMOJI_PATTERN = re.compile(r'[\U0001F300-\U0001F9FF\U0001FA00-\U0001FAFF\u2600-\u26FF\u2700-\u27BF]')
INSTAGRAM_USERNAME = re.compile(r'@[a-zA-Z0-9._]+')
FACEBOOK_USERNAME = re.compile(r'facebook\.com/[a-zA-Z0-9._-]+')
LINKEDIN_USERNAME = re.compile(r'linkedin\.com/in/[a-zA-Z0-9._-]+')
TELEGRAM_USERNAME = re.compile(r'@[a-zA-Z0-9_]+')
DISCORD_USERNAME = re.compile(r'[a-zA-Z0-9_]+#\d{4}')
SLACK_USERNAME = re.compile(r'@[a-zA-Z0-9._-]+')
WHATSAPP_USERNAME = re.compile(r'wa\.me/\d+')
GEOJSON_PATTERN = re.compile(r'\{"type"\s*:\s*"Point"\s*,\s*"coordinates"\s*:\s*\[-?\d+\.?\d*,\s*-?\d+\.?\d*\]\}')
DMS_PATTERN = re.compile(r'\d+°\d+\'\d+\.?\d*"[NS]\s+\d+°\d+\'\d+\.?\d*"[EW]')

# Social media platforms
SOCIAL_PLATFORMS = {
    'INSTAGRAM': ['instagram.com', 'instagr.am'],
    'FACEBOOK': ['facebook.com', 'fb.com'],
    'LINKEDIN': ['linkedin.com'],
    'TELEGRAM': ['t.me', 'telegram.org'],
    'DISCORD': ['discord.com', 'discord.gg'],
    'SLACK': ['slack.com'],
    'WHATSAPP': ['wa.me', 'whatsapp.com'],
    'TWITTER': ['twitter.com', 'x.com'],
    'TIKTOK': ['tiktok.com'],
    'YOUTUBE': ['youtube.com', 'youtu.be'],
    'REDDIT': ['reddit.com'],
    'SNAPCHAT': ['snapchat.com'],
}

def generate_url_examples(count: int) -> List[Dict]:
    """Generate URL examples."""
    examples = []
    domains = ['example.com', 'test.org', 'malicious.io', 'suspicious.net', 'company.com']
    paths = ['/page', '/user/profile', '/api/v1/data', '/download/file', '/search?q=test']
    
    for i in range(count):
        domain = random.choice(domains)
        path = random.choice(paths)
        url = f"https://{domain}{path}"
        
        contexts = [
            f"Investigate URL {url} for suspicious activity",
            f"Block access to {url}",
            f"URL {url} flagged for phishing",
            f"Monitor traffic to {url}",
            f"URL {url} associated with malware",
            f"Scan {url} for vulnerabilities",
            f"URL {url} linked to threat actor",
            f"Check {url} reputation",
            f"URL {url} used in attack campaign",
            f"Analyze {url} content"
        ]
        text = random.choice(contexts)
        match = URL_PATTERN.search(text)
        if match:
            examples.append({
                'text': text,
                'entities': [[match.start(), match.end(), 'URL']]
            })
    return examples

def generate_ipv6_examples(count: int) -> List[Dict]:
    """Generate IPv6 address examples."""
    examples = []
    for i in range(count):
        # Generate random IPv6
        ipv6 = ':'.join([f"{random.randint(0, 65535):x}" for _ in range(8)])
        # Sometimes use compressed format
        if random.random() < 0.3:
            ipv6 = ipv6.replace(':0000:', '::', 1)
        
        contexts = [
            f"Block IPv6 address {ipv6}",
            f"Traffic from {ipv6} detected",
            f"IPv6 {ipv6} associated with attack",
            f"Monitor {ipv6} for suspicious activity",
            f"IPv6 address {ipv6} flagged",
            f"Trace connections from {ipv6}",
            f"IPv6 {ipv6} linked to threat actor",
            f"Investigate {ipv6} network activity",
            f"IPv6 {ipv6} used in DDoS attack",
            f"Block {ipv6} at firewall"
        ]
        text = random.choice(contexts)
        match = IPV6_PATTERN.search(text)
        if match:
            examples.append({
                'text': text,
                'entities': [[match.start(), match.end(), 'IPV6_ADDRESS']]
            })
    return examples

def generate_international_phone_examples(count: int) -> List[Dict]:
    """Generate international phone number examples."""
    examples = []
    formats = [
        lambda: f"+{random.randint(1,99)}-{random.randint(10,99)}-{random.randint(100,999)}-{random.randint(1000,9999)}",
        lambda: f"+{random.randint(1,99)} {random.randint(10,99)} {random.randint(100,999)} {random.randint(1000,9999)}",
        lambda: f"+{random.randint(1,99)} ({random.randint(10,99)}) {random.randint(100,999)}-{random.randint(1000,9999)}",
        lambda: f"00{random.randint(1,99)} {random.randint(10,99)} {random.randint(100,999)} {random.randint(1000,9999)}",
    ]
    
    countries = ['+1', '+44', '+33', '+49', '+81', '+86', '+91', '+7', '+61', '+55']
    
    for i in range(count):
        country = random.choice(countries)
        phone = f"{country}-{random.randint(10,99)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
        
        contexts = [
            f"Phone number {phone} linked to suspect",
            f"Investigate {phone} for fraud",
            f"Phone {phone} used in social engineering",
            f"Monitor calls from {phone}",
            f"Phone number {phone} flagged",
            f"Trace {phone} ownership",
            f"Phone {phone} associated with threat",
            f"Verify {phone} registration",
            f"Phone number {phone} in contact list",
            f"Block {phone} communications"
        ]
        text = random.choice(contexts)
        # Simple phone pattern match
        phone_clean = phone.replace('-', ' ').replace('(', '').replace(')', '')
        idx = text.find(phone)
        if idx != -1:
            examples.append({
                'text': text,
                'entities': [[idx, idx + len(phone), 'PHONE_NUMBER']]
            })
    return examples

def generate_emoji_examples(count: int) -> List[Dict]:
    """Generate emoji examples."""
    examples = []
    emojis = ['😀', '😃', '😄', '😁', '😆', '😅', '🤣', '😂', '🙂', '🙃', 
              '😉', '😊', '😇', '🥰', '😍', '🤩', '😘', '😗', '😚', '😙',
              '😋', '😛', '😜', '🤪', '😝', '🤑', '🤗', '🤭', '🤫', '🤔',
              '🤐', '🤨', '😐', '😑', '😶', '😏', '😒', '🙄', '😬', '🤥',
              '😌', '😔', '😪', '🤤', '😴', '😷', '🤒', '🤕', '🤢', '🤮',
              '🤧', '🥵', '🥶', '😵', '🤯', '🤠', '🥳', '😎', '🤓', '🧐',
              '⚠️', '🚨', '🔒', '🔓', '🛡️', '⚔️', '💣', '🔪', '🗡️', '🏹',
              '🛡️', '🔐', '🔑', '🗝️', '💻', '🖥️', '📱', '⌚', '💾', '💿']
    
    for i in range(count):
        emoji = random.choice(emojis)
        contexts = [
            f"Message contains {emoji} emoji",
            f"User posted {emoji} in chat",
            f"Emoji {emoji} detected in communication",
            f"Social media post with {emoji}",
            f"Message includes {emoji} symbol",
            f"Emoji {emoji} used in context",
            f"Communication contains {emoji}",
            f"Post includes {emoji} emoji",
            f"Message has {emoji} symbol",
            f"Emoji {emoji} found in text"
        ]
        text = random.choice(contexts)
        match = EMOJI_PATTERN.search(text)
        if match:
            examples.append({
                'text': text,
                'entities': [[match.start(), match.end(), 'EMOJI']]
            })
    return examples

def generate_social_username_examples(count: int) -> List[Dict]:
    """Generate social media username examples."""
    examples = []
    platforms = ['INSTAGRAM', 'FACEBOOK', 'LINKEDIN', 'TELEGRAM', 'DISCORD', 'SLACK', 'WHATSAPP']
    
    for i in range(count):
        platform = random.choice(platforms)
        username = f"user{random.randint(1,999)}"
        
        if platform == 'INSTAGRAM':
            username_text = f"@{username}"
            pattern = INSTAGRAM_USERNAME
        elif platform == 'FACEBOOK':
            username_text = f"facebook.com/{username}"
            pattern = FACEBOOK_USERNAME
        elif platform == 'LINKEDIN':
            username_text = f"linkedin.com/in/{username}"
            pattern = LINKEDIN_USERNAME
        elif platform == 'TELEGRAM':
            username_text = f"@{username}"
            pattern = TELEGRAM_USERNAME
        elif platform == 'DISCORD':
            username_text = f"{username}#{random.randint(1000,9999)}"
            pattern = DISCORD_USERNAME
        elif platform == 'SLACK':
            username_text = f"@{username}"
            pattern = SLACK_USERNAME
        else:  # WHATSAPP
            username_text = f"wa.me/{random.randint(1000000000,9999999999)}"
            pattern = WHATSAPP_USERNAME
        
        contexts = [
            f"Investigate {platform.lower()} account {username_text}",
            f"Monitor {username_text} activity",
            f"Account {username_text} linked to threat",
            f"Profile {username_text} flagged",
            f"User {username_text} under investigation",
            f"Account {username_text} associated with attack",
            f"Track {username_text} communications",
            f"Profile {username_text} suspicious",
            f"User {username_text} in contact list",
            f"Account {username_text} verified"
        ]
        text = random.choice(contexts)
        match = pattern.search(text)
        if match:
            examples.append({
                'text': text,
                'entities': [[match.start(), match.end(), f'{platform}_USERNAME']]
            })
    return examples

def generate_social_url_examples(count: int) -> List[Dict]:
    """Generate social media URL examples."""
    examples = []
    
    for i in range(count):
        platform = random.choice(list(SOCIAL_PLATFORMS.keys()))
        domain = random.choice(SOCIAL_PLATFORMS[platform])
        username = f"user{random.randint(1,999)}"
        url = f"https://{domain}/{username}"
        
        contexts = [
            f"Profile URL {url} under investigation",
            f"Monitor {url} for suspicious activity",
            f"URL {url} linked to threat actor",
            f"Social media profile {url} flagged",
            f"Investigate {url} account",
            f"URL {url} associated with attack",
            f"Track {url} activity",
            f"Profile {url} suspicious",
            f"Account {url} in contact list",
            f"URL {url} verified"
        ]
        text = random.choice(contexts)
        match = URL_PATTERN.search(text)
        if match:
            examples.append({
                'text': text,
                'entities': [[match.start(), match.end(), f'{platform}_URL']]
            })
    return examples

def generate_geojson_examples(count: int) -> List[Dict]:
    """Generate GeoJSON coordinate examples."""
    examples = []
    
    for i in range(count):
        lon = round(random.uniform(-180, 180), 6)
        lat = round(random.uniform(-90, 90), 6)
        geojson = f'{{"type": "Point", "coordinates": [{lon}, {lat}]}}'
        
        contexts = [
            f"Location data: {geojson}",
            f"GeoJSON coordinates {geojson} extracted",
            f"Point location {geojson} identified",
            f"Geographic data {geojson} found",
            f"Coordinates in GeoJSON format: {geojson}",
            f"Location {geojson} verified",
            f"GeoJSON {geojson} from satellite",
            f"Point {geojson} on map",
            f"Geographic position {geojson}",
            f"Coordinates {geojson} confirmed"
        ]
        text = random.choice(contexts)
        match = GEOJSON_PATTERN.search(text)
        if match:
            examples.append({
                'text': text,
                'entities': [[match.start(), match.end(), 'GEOJSON']]
            })
    return examples

def generate_dms_examples(count: int) -> List[Dict]:
    """Generate DMS (Degrees, Minutes, Seconds) coordinate examples."""
    examples = []
    
    for i in range(count):
        lat_deg = random.randint(0, 90)
        lat_min = random.randint(0, 59)
        lat_sec = round(random.uniform(0, 59.99), 2)
        lat_dir = random.choice(['N', 'S'])
        
        lon_deg = random.randint(0, 180)
        lon_min = random.randint(0, 59)
        lon_sec = round(random.uniform(0, 59.99), 2)
        lon_dir = random.choice(['E', 'W'])
        
        dms = f"{lat_deg}°{lat_min}'{lat_sec}\"{lat_dir} {lon_deg}°{lon_min}'{lon_sec}\"{lon_dir}"
        
        contexts = [
            f"Coordinates {dms} identified",
            f"Location at {dms}",
            f"DMS format: {dms}",
            f"Position {dms} verified",
            f"Coordinates {dms} from GPS",
            f"Location {dms} confirmed",
            f"DMS {dms} extracted",
            f"Position {dms} on map",
            f"Coordinates {dms} found",
            f"Location {dms} validated"
        ]
        text = random.choice(contexts)
        match = DMS_PATTERN.search(text)
        if match:
            examples.append({
                'text': text,
                'entities': [[match.start(), match.end(), 'DMS_COORDINATES']]
            })
    return examples

def generate_custom_coordinate_examples(count: int) -> List[Dict]:
    """Generate custom coordinate format examples."""
    examples = []
    
    for i in range(count):
        lat = round(random.uniform(-90, 90), 6)
        lon = round(random.uniform(-180, 180), 6)
        
        formats = [
            f'{{"location": {{"latitude": {lat}, "longitude": {lon}}}}}',
            f'{{"lat": {lat}, "lng": {lon}}}',
            f'{{"coordinates": {{"lat": {lat}, "lon": {lon}}}}}',
            f'lat:{lat},lon:{lon}',
            f'latitude={lat}&longitude={lon}',
        ]
        
        coord_text = random.choice(formats)
        contexts = [
            f"Location data: {coord_text}",
            f"Coordinates {coord_text} extracted",
            f"Custom format: {coord_text}",
            f"Location {coord_text} identified",
            f"Coordinates {coord_text} found",
            f"Position {coord_text} verified",
            f"Location {coord_text} confirmed",
            f"Coordinates {coord_text} from API",
            f"Location {coord_text} validated",
            f"Coordinates {coord_text} parsed"
        ]
        text = random.choice(contexts)
        # Find coordinates in text
        idx = text.find(coord_text)
        if idx != -1:
            examples.append({
                'text': text,
                'entities': [[idx, idx + len(coord_text), 'CUSTOM_COORDINATES']]
            })
    return examples

def add_to_file(file_path: Path, examples: List[Dict], entity_type: str):
    """Add examples to a file."""
    with open(file_path, 'a', encoding='utf-8') as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')

def main():
    """Main function."""
    base_dir = Path('cyber-train/entities-intent')
    if not base_dir.exists():
        base_dir = Path('entities-intent')
    
    entity_files = list(base_dir.rglob('*_entities.jsonl'))
    file_map = {f.name: f for f in entity_files}
    
    # Target files for each entity type
    target_files = {
        'URL': [
            'cybint_entities.jsonl',
            'comint_entities.jsonl',
            'threat_intel_entities.jsonl',
            'incident_response_entities.jsonl',
            'network_security_entities.jsonl',
        ],
        'IPV6_ADDRESS': [
            'network_security_entities.jsonl',
            'cybint_entities.jsonl',
            'threat_intel_entities.jsonl',
            'incident_response_entities.jsonl',
        ],
        'PHONE_NUMBER': [  # International phone numbers
            'comint_entities.jsonl',
            'humint_entities.jsonl',
            'socmint_entities.jsonl',
            'data_privacy_sovereignty_entities.jsonl',
        ],
        'EMOJI': [
            'socmint_entities.jsonl',
            'comint_entities.jsonl',
            'humint_entities.jsonl',
        ],
        'INSTAGRAM_USERNAME': [
            'socmint_entities.jsonl',
            'comint_entities.jsonl',
        ],
        'FACEBOOK_USERNAME': [
            'socmint_entities.jsonl',
            'comint_entities.jsonl',
        ],
        'LINKEDIN_USERNAME': [
            'socmint_entities.jsonl',
            'humint_entities.jsonl',
        ],
        'TELEGRAM_USERNAME': [
            'comint_entities.jsonl',
            'socmint_entities.jsonl',
        ],
        'DISCORD_USERNAME': [
            'comint_entities.jsonl',
            'socmint_entities.jsonl',
        ],
        'SLACK_USERNAME': [
            'comint_entities.jsonl',
            'cybint_entities.jsonl',
        ],
        'WHATSAPP_USERNAME': [
            'comint_entities.jsonl',
            'socmint_entities.jsonl',
        ],
        'INSTAGRAM_URL': [
            'socmint_entities.jsonl',
            'comint_entities.jsonl',
        ],
        'FACEBOOK_URL': [
            'socmint_entities.jsonl',
            'comint_entities.jsonl',
        ],
        'LINKEDIN_URL': [
            'socmint_entities.jsonl',
            'humint_entities.jsonl',
        ],
        'TELEGRAM_URL': [
            'comint_entities.jsonl',
            'socmint_entities.jsonl',
        ],
        'DISCORD_URL': [
            'comint_entities.jsonl',
            'socmint_entities.jsonl',
        ],
        'SLACK_URL': [
            'comint_entities.jsonl',
            'cybint_entities.jsonl',
        ],
        'WHATSAPP_URL': [
            'comint_entities.jsonl',
            'socmint_entities.jsonl',
        ],
        'GEOJSON': [
            'geoint_entities.jsonl',
            'imint_entities.jsonl',
            'ai-int_entities.jsonl',
        ],
        'DMS_COORDINATES': [
            'geoint_entities.jsonl',
            'imint_entities.jsonl',
        ],
        'CUSTOM_COORDINATES': [
            'geoint_entities.jsonl',
            'imint_entities.jsonl',
            'ai-int_entities.jsonl',
        ],
    }
    
    # Entity generators
    entity_generators = {
        'URL': (generate_url_examples, 300),
        'IPV6_ADDRESS': (generate_ipv6_examples, 200),
        'PHONE_NUMBER': (generate_international_phone_examples, 200),
        'EMOJI': (generate_emoji_examples, 200),
        'INSTAGRAM_USERNAME': (lambda c: generate_social_username_examples(c), 100),
        'FACEBOOK_USERNAME': (lambda c: generate_social_username_examples(c), 100),
        'LINKEDIN_USERNAME': (lambda c: generate_social_username_examples(c), 100),
        'TELEGRAM_USERNAME': (lambda c: generate_social_username_examples(c), 100),
        'DISCORD_USERNAME': (lambda c: generate_social_username_examples(c), 100),
        'SLACK_USERNAME': (lambda c: generate_social_username_examples(c), 100),
        'WHATSAPP_USERNAME': (lambda c: generate_social_username_examples(c), 100),
        'INSTAGRAM_URL': (lambda c: generate_social_url_examples(c), 100),
        'FACEBOOK_URL': (lambda c: generate_social_url_examples(c), 100),
        'LINKEDIN_URL': (lambda c: generate_social_url_examples(c), 100),
        'TELEGRAM_URL': (lambda c: generate_social_url_examples(c), 100),
        'DISCORD_URL': (lambda c: generate_social_url_examples(c), 100),
        'SLACK_URL': (lambda c: generate_social_url_examples(c), 100),
        'WHATSAPP_URL': (lambda c: generate_social_url_examples(c), 100),
        'GEOJSON': (generate_geojson_examples, 200),
        'DMS_COORDINATES': (generate_dms_examples, 200),
        'CUSTOM_COORDINATES': (generate_custom_coordinate_examples, 200),
    }
    
    print("="*80)
    print("ADDING ADDITIONAL ENTITY EXAMPLES")
    print("="*80)
    
    total_added = {}
    
    for entity_type, (generator_func, total_count) in entity_generators.items():
        if entity_type not in target_files:
            continue
            
        print(f"\n{'='*80}")
        print(f"Adding {entity_type} examples ({total_count} total)")
        print(f"{'='*80}")
        
        examples = generator_func(total_count)
        files_for_type = target_files[entity_type]
        examples_per_file = total_count // len(files_for_type)
        remainder = total_count % len(files_for_type)
        
        added_count = 0
        for i, filename in enumerate(files_for_type):
            if filename not in file_map:
                print(f"  ⚠️  File not found: {filename}")
                continue
            file_path = file_map[filename]
            
            count_for_file = examples_per_file + (1 if i < remainder else 0)
            file_examples = examples[added_count:added_count + count_for_file]
            add_to_file(file_path, file_examples, entity_type)
            added_count += len(file_examples)
            print(f"  ✅ Added {len(file_examples)} examples to {file_path.name}")
        
        total_added[entity_type] = added_count
    
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    for entity_type, count in total_added.items():
        print(f"  {entity_type}: {count} examples added")
    
    print(f"\n✅ Total examples added: {sum(total_added.values())}")

if __name__ == '__main__':
    main()

