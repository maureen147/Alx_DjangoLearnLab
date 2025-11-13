#!/usr/bin/env python
settings_file = 'LibraryProject/LibraryProject/settings.py'

# Read the file
with open(settings_file, 'r') as f:
    content = f.read()

# Check if SECURE_PROXY_SSL_HEADER already exists
if 'SECURE_PROXY_SSL_HEADER' not in content:
    # Find where to insert - after other SECURE_ settings
    lines = content.split('\n')
    
    # Find the position after SECURE_REFERRER_POLICY
    insert_position = None
    for i, line in enumerate(lines):
        if 'SECURE_REFERRER_POLICY' in line:
            insert_position = i + 1
            break
    
    # If not found, find any SECURE_ setting
    if insert_position is None:
        for i, line in enumerate(lines):
            if line.strip().startswith('SECURE_'):
                insert_position = i + 1
                break
    
    # If still not found, add after security headers section
    if insert_position is None:
        for i, line in enumerate(lines):
            if 'X_FRAME_OPTIONS' in line:
                insert_position = i + 1
                break
    
    # Add the SECURE_PROXY_SSL_HEADER configuration
    proxy_config = '''# SECURITY: Proxy SSL Header - Required when behind a reverse proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')'''
    
    if insert_position is not None:
        lines.insert(insert_position, proxy_config)
        new_content = '\n'.join(lines)
        
        with open(settings_file, 'w') as f:
            f.write(new_content)
        print("✅ Added SECURE_PROXY_SSL_HEADER to settings.py")
    else:
        print("❌ Could not find appropriate position to insert SECURE_PROXY_SSL_HEADER")
else:
    print("✅ SECURE_PROXY_SSL_HEADER already exists")
