import re

settings_file = 'LibraryProject/LibraryProject/settings.py'

with open(settings_file, 'r') as f:
    content = f.read()

# Remove duplicate ROOT_URLCONF lines and fix the path
# Keep only one instance with the correct path
content = re.sub(r"ROOT_URLCONF = 'LibraryProject\.urls'\n", '', content)
content = re.sub(r"ROOT_URLCONF = 'LibraryProject\.urls'", "ROOT_URLCONF = 'LibraryProject.LibraryProject.urls'", content)

# If no ROOT_URLCONF found, add it
if 'ROOT_URLCONF' not in content:
    # Add after other settings
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'WSGI_APPLICATION' in line:
            lines.insert(i, "ROOT_URLCONF = 'LibraryProject.LibraryProject.urls'")
            break
    content = '\n'.join(lines)

with open(settings_file, 'w') as f:
    f.write(content)

print("✅ Fixed ROOT_URLCONF - removed duplicates and set correct path")
