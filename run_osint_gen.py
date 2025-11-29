#!/usr/bin/env python3
"""Simple runner for OSINT generation."""
import subprocess
import sys

result = subprocess.run([sys.executable, 'create_osint_realistic.py'], 
                       capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)
print(f"Return code: {result.returncode}")

