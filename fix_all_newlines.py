import os
import re

def fix_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False
    
    original_content = content
    
    # Replace old normalization (removing newlines) with new one (replacing with spaces)
    old_pattern = r'\.replace\(/\\n/g, ""\)'
    def replace_func(match):
        return '.replace(/\\n/g, " ").replace(/\\s+/g, " ").trim()'
    
    new_content = re.sub(old_pattern, replace_func, content)
    
    if new_content != content:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        except Exception as e:
            print(f"Error writing {filepath}: {e}")
            return False
    return False

# Find all HTML files in docs directory
html_files = []
for root, dirs, files in os.walk('docs'):
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

updated_count = 0
for filepath in html_files:
    # Check if file has the old normalization pattern
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        if '.replace(/\\n/g, "")' in content:
            if fix_file(filepath):
                updated_count += 1
                print(f"Updated: {filepath}")

print(f"\nTotal files updated: {updated_count}")
