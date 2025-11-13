#!/usr/bin/env python
# -*- coding: utf-8 -*-

settings_file = 'LibraryProject/LibraryProject/settings.py'

try:
    # Try reading with UTF-8 encoding
    with open(settings_file, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError:
    try:
        # Try reading with Latin-1 encoding as fallback
        with open(settings_file, 'r', encoding='latin-1') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Last resort: read as bytes and replace problematic characters
        with open(settings_file, 'rb') as f:
            content_bytes = f.read()
        content = content_bytes.decode('utf-8', errors='replace')

# Check if SECURE_PROXY_SSL_HEADER already exists
if 'SECURE_PROXY_SSL_HEADER' not in content:
    # Find where to insert - look for SECURE_REFERRER_POLICY
    lines = content.split('\n')
    
    insert_position = None
    for i, line in enumerate(lines):
        if 'SECURE_REFERRER_POLICY' in line:
            insert_position = i + 1
            break
    
    # Add the SECURE_PROXY_SSL_HEADER configuration
    proxy_config = '''# SECURITY: Proxy SSL Header - Required when behind a reverse proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')'''
    
    if insert_position is not None:
        lines.insert(insert_position, proxy_config)
        
        # Write back with UTF-8 encoding
        with open(settings_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        print("✅ Added SECURE_PROXY_SSL_HEADER to settings.py")
        print("✅ Fixed file encoding to UTF-8")
    else:
        print("❌ Could not find SECURE_REFERRER_POLICY to insert after")
else:
    print("✅ SECURE_PROXY_SSL_HEADER already exists")
