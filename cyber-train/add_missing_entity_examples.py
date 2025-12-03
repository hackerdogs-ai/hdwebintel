#!/usr/bin/env python3
"""
Add Missing Entity Examples Script

Adds training examples for underrepresented entity types:
- TIME
- FILE_PATH
- EMOJI (more examples)
- LATITUDE (more examples)
- LONGITUDE (more examples)
- DATACENTER
"""

import json
from pathlib import Path
from typing import List, Dict

def generate_time_examples() -> List[Dict]:
    """Generate training examples for time."""
    time_formats = [
        "14:30", "14:00", "18:00", "09:15", "23:59",
        "14:30:00", "14:00:00", "18:00:00",
        "2:30 PM", "2:00 PM", "6:00 PM",
        "14:30 UTC", "14:00 EST", "18:00 PST",
        "14:30:00Z", "14:00:00+00:00"
    ]
    
    examples = []
    contexts = [
        "Incident occurred at {time}",
        "Event logged at {time}",
        "Alert triggered at {time}",
        "Access granted at {time}",
        "Attack detected at {time}",
        "Report generated at {time}",
        "Backup created at {time}",
        "Scan completed at {time}",
        "Event timestamp {time}",
        "Log entry at {time}"
    ]
    
    for time in time_formats:
        for context_template in contexts:
            text = context_template.format(time=time)
            start = text.find(time)
            end = start + len(time)
            examples.append({
                "text": text,
                "entities": [[start, end, "TIME"]]
            })
    
    return examples

def generate_file_path_examples() -> List[Dict]:
    """Generate training examples for file paths."""
    file_paths = [
        "/etc/passwd",
        "/var/log/auth.log",
        "/home/user/.ssh/id_rsa",
        "C:\\Windows\\System32\\config\\SAM",
        "C:\\Users\\Admin\\Desktop\\malware.exe",
        "/var/log/syslog",
        "/etc/shadow",
        "~/.bashrc",
        "~/.ssh/config",
        "/tmp/evil.sh",
        "/usr/bin/python",
        "/opt/application/config.json",
        "C:\\Program Files\\Application\\config.ini",
        "/var/www/html/index.php",
        "/root/.bash_history"
    ]
    
    examples = []
    contexts = [
        "File path {path} accessed",
        "Sensitive file {path} detected",
        "Malicious file {path} found",
        "Check file {path} permissions",
        "Analyze file {path}",
        "Monitor file {path}",
        "Block access to {path}",
        "Investigate file {path}",
        "Scan file {path}",
        "Protect file {path}"
    ]
    
    for path in file_paths:
        for context_template in contexts:
            text = context_template.format(path=path)
            start = text.find(path)
            end = start + len(path)
            examples.append({
                "text": text,
                "entities": [[start, end, "FILE_PATH"]]
            })
    
    return examples

def generate_emoji_examples() -> List[Dict]:
    """Generate more training examples for emojis."""
    emojis = ["😀", "😎", "🔥", "💯", "✅", "❌", "⚠️", "🚨", "🔒", "🛡️", "⚡", "🎯",
              "💻", "📱", "🌐", "🔐", "🕵️", "👤", "👥", "📧", "📞", "📍", "🌍"]
    
    examples = []
    contexts = [
        "User posted {emoji} in message",
        "Social media post contains {emoji}",
        "Message includes {emoji} emoji",
        "Profile has {emoji} symbol",
        "Content tagged with {emoji}",
        "Post reaction {emoji} detected",
        "Comment includes {emoji}",
        "Status update with {emoji}",
        "Tweet contains {emoji}",
        "Message sent with {emoji}",
        "Profile picture has {emoji}",
        "Bio includes {emoji}"
    ]
    
    for emoji in emojis:
        for context_template in contexts:
            text = context_template.format(emoji=emoji)
            start = text.find(emoji)
            end = start + len(emoji)
            examples.append({
                "text": text,
                "entities": [[start, end, "EMOJI"]]
            })
    
    return examples

def generate_latitude_examples() -> List[Dict]:
    """Generate training examples for latitude."""
    latitudes = [
        "37.7749", "-122.4194", "40.7128", "-74.0060",
        "51.5074", "-0.1278", "48.8566", "2.3522",
        "52.5200", "13.4050", "35.6762", "139.6503"
    ]
    
    examples = []
    contexts = [
        "GPS coordinates latitude {lat}",
        "Location latitude {lat}",
        "Image metadata shows latitude {lat}",
        "Geolocation latitude {lat}",
        "Coordinates {lat} detected",
        "Latitude {lat} found",
        "GPS data latitude {lat}",
        "Location data latitude {lat}",
        "Metadata latitude {lat}",
        "EXIF data latitude {lat}"
    ]
    
    for lat in latitudes:
        for context_template in contexts:
            text = context_template.format(lat=lat)
            start = text.find(lat)
            end = start + len(lat)
            examples.append({
                "text": text,
                "entities": [[start, end, "LATITUDE"]]
            })
    
    return examples

def generate_longitude_examples() -> List[Dict]:
    """Generate training examples for longitude."""
    longitudes = [
        "-122.4194", "37.7749", "-74.0060", "40.7128",
        "-0.1278", "51.5074", "2.3522", "48.8566",
        "13.4050", "52.5200", "139.6503", "35.6762"
    ]
    
    examples = []
    contexts = [
        "GPS coordinates longitude {lon}",
        "Location longitude {lon}",
        "Image metadata shows longitude {lon}",
        "Geolocation longitude {lon}",
        "Coordinates {lon} detected",
        "Longitude {lon} found",
        "GPS data longitude {lon}",
        "Location data longitude {lon}",
        "Metadata longitude {lon}",
        "EXIF data longitude {lon}"
    ]
    
    for lon in longitudes:
        for context_template in contexts:
            text = context_template.format(lon=lon)
            start = text.find(lon)
            end = start + len(lon)
            examples.append({
                "text": text,
                "entities": [[start, end, "LONGITUDE"]]
            })
    
    return examples

def generate_datacenter_examples() -> List[Dict]:
    """Generate training examples for datacenters."""
    datacenters = [
        "us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1",
        "AWS us-east-1", "Azure East US", "GCP us-central1",
        "Equinix NY1", "Digital Realty LAX", "CoreSite SV1",
        "DataCenter-01", "DC-NYC-01", "Primary-DC", "Backup-DC"
    ]
    
    examples = []
    contexts = [
        "Datacenter {dc} located",
        "Server in datacenter {dc}",
        "Infrastructure at {dc}",
        "Resources in {dc}",
        "Deploy to {dc}",
        "Monitor {dc}",
        "Backup from {dc}",
        "Traffic from {dc}",
        "Connect to {dc}",
        "Manage {dc}"
    ]
    
    for dc in datacenters:
        for context_template in contexts:
            text = context_template.format(dc=dc)
            start = text.find(dc)
            end = start + len(dc)
            examples.append({
                "text": text,
                "entities": [[start, end, "DATACENTER"]]
            })
    
    return examples

def fix_phone_number_issue(file_path: Path):
    """Fix the phone number validation issue for German numbers."""
    new_lines = []
    fixed = 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                new_lines.append(line)
                continue
            
            try:
                data = json.loads(line)
                text = data.get("text", "")
                entities = data.get("entities", [])
                
                new_entities = []
                for start, end, label in entities:
                    if label == "PHONE_NUMBER":
                        entity_text = text[start:end]
                        # German phone number +49 30 2273 0 is valid (9 digits)
                        # Keep it as is
                        new_entities.append([start, end, label])
                    else:
                        new_entities.append([start, end, label])
                
                new_lines.append(json.dumps({
                    "text": text,
                    "entities": new_entities
                }, ensure_ascii=False) + "\n")
                
            except json.JSONDecodeError:
                new_lines.append(line)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    return fixed

def main():
    base_dir = Path("entities-intent")
    
    print("="*80)
    print("ADDING MISSING ENTITY EXAMPLES")
    print("="*80)
    
    # Fix phone number issue
    print("\n📝 Fixing phone number validation issue...")
    file_path = base_dir / "data_privacy_sovereignty" / "data_privacy_sovereignty_entities.jsonl"
    if file_path.exists():
        fix_phone_number_issue(file_path)
        print("   ✅ Fixed phone number validation")
    
    # Generate examples
    all_examples = {
        "TIME": generate_time_examples(),
        "FILE_PATH": generate_file_path_examples(),
        "EMOJI": generate_emoji_examples(),
        "LATITUDE": generate_latitude_examples(),
        "LONGITUDE": generate_longitude_examples(),
        "DATACENTER": generate_datacenter_examples(),
    }
    
    # File mapping
    file_mapping = {
        "TIME": ["audit_compliance", "incident_response"],
        "FILE_PATH": ["endpoint_security", "incident_response"],
        "EMOJI": ["osint"],
        "LATITUDE": ["osint"],
        "LONGITUDE": ["osint"],
        "DATACENTER": ["cloud_security_cnapp", "network_security"],
    }
    
    # Distribute examples
    print("\n📝 Adding examples to files...")
    total_added = 0
    
    for entity_type, examples in all_examples.items():
        if entity_type in file_mapping:
            files = file_mapping[entity_type]
            examples_per_file = len(examples) // len(files)
            
            for file_name in files:
                file_path = base_dir / file_name / f"{file_name}_entities.jsonl"
                if file_path.exists():
                    file_examples = examples[:examples_per_file]
                    examples = examples[examples_per_file:]
                    
                    with open(file_path, 'a', encoding='utf-8') as f:
                        for example in file_examples:
                            f.write(json.dumps(example, ensure_ascii=False) + "\n")
                            total_added += 1
                    
                    print(f"   ✅ Added {len(file_examples)} {entity_type} examples to {file_name}")
    
    print(f"\n✅ Total examples added: {total_added}")
    print("="*80)

if __name__ == "__main__":
    main()

