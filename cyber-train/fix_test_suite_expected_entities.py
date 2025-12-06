#!/usr/bin/env python3
"""
Fix invalid expected entities in test suite.
This script corrects the test suite expected entities based on review findings.
"""

import re
from pathlib import Path

# Invalid entities found and their corrections
FIXES = {
    # Invalid hashes - these are too short or invalid format
    'abc123': None,  # Remove - invalid hash (too short)
    'def456': None,  # Remove - invalid hash (too short)
    'ghi789': None,  # Remove - invalid hash (too short)
    'abc123def456': None,  # Remove - invalid hash (too short for MD5)
    'ghi789jkl012': None,  # Remove - invalid hash (too short for SHA256)
    
    # Invalid dates - Unix timestamps should not be DATE
    '1701350400': None,  # Remove - Unix timestamp, not a date
    '1701350400.123': None,  # Remove - Unix timestamp, not a date
    '30-Nov-2024': ('2024-11-30', 'DATE'),  # Fix format
    
    # Invalid URLs - these need protocol or are file paths
    'sftp://secure.example.com': ('sftp://secure.example.com/file', 'URL'),  # Add path
    'file:///local/path': None,  # Remove - file:// URLs are not standard
    'HTTP://example.com/path': ('http://example.com/path', 'URL'),  # Fix case
    
    # Invalid CVE - missing hyphens
    'CVE202144228': ('CVE-2021-44228', 'CVE_ID'),  # Fix format
}

def fix_test_suite():
    """Fix test suite expected entities."""
    test_file = Path("generate_comprehensive_test_cases.py")
    
    if not test_file.exists():
        print(f"⚠️  Test suite file not found: {test_file}")
        return
    
    # Read file
    with open(test_file, 'r') as f:
        content = f.read()
    
    fixes_applied = 0
    
    # Apply fixes
    for old_entity, fix in FIXES.items():
        if fix is None:
            # Remove entity
            # Find patterns like ("old_entity", "LABEL") or [("old_entity", "LABEL")]
            pattern = re.compile(rf'\(\s*["\']{re.escape(old_entity)}["\']\s*,\s*["\'][^"\']+["\']\s*\)')
            matches = pattern.findall(content)
            if matches:
                for match in matches:
                    # Remove the tuple
                    content = content.replace(match, '')
                    fixes_applied += 1
                    # Clean up trailing commas
                    content = re.sub(r',\s*,', ',', content)
                    content = re.sub(r',\s*\]', ']', content)
                    content = re.sub(r',\s*\)', ')', content)
        else:
            # Replace entity
            new_entity, new_label = fix
            pattern = rf'\(\s*["\']{re.escape(old_entity)}["\']\s*,\s*["\'][^"\']+["\']\s*\)'
            replacement = f'("{new_entity}", "{new_label}")'
            content = re.sub(pattern, replacement, content)
            fixes_applied += len(re.findall(pattern, content))
    
    # Write fixed file
    with open(test_file, 'w') as f:
        f.write(content)
    
    print(f"✅ Applied {fixes_applied} fixes to test suite")
    return fixes_applied

def main():
    print("="*80)
    print("FIX TEST SUITE EXPECTED ENTITIES")
    print("="*80)
    print("\nFixing invalid expected entities:")
    print("  - Removing invalid hashes (too short)")
    print("  - Removing Unix timestamps (not dates)")
    print("  - Fixing invalid URL formats")
    print("  - Fixing invalid CVE formats")
    print("  - Fixing invalid date formats")
    print()
    
    fixes = fix_test_suite()
    
    print(f"\n✅ Fixed {fixes} invalid expected entities")
    print("="*80)

if __name__ == "__main__":
    main()

