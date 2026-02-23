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
    
    # Replace all existing normalization patterns with simple whitespace removal
    # Pattern 1: .replace(/\n/g, " ").replace(/\s+/g, " ").trim()
    content = content.replace('.replace(/\\n/g, " ").replace(/\\s+/g, " ").trim()', '.replace(/\\s/g, "")')
    
    # Pattern 2: .replace(/\n/g, "")
    content = content.replace('.replace(/\\n/g, "")', '.replace(/\\s/g, "")')
    
    # Pattern 3: if(a==expectedAnswer) without normalization
    def add_normalization_equals(match):
        full_match = match.group(0)
        expected = match.group(1)
        # Skip if already has normalization
        if '.replace(/\\s/g, "")' in full_match:
            return full_match
        return f'if(a.replace(/\\s/g, "")=={expected}.replace(/\\s/g, ""))'
    
    # Pattern 4: if(a!=choice1) without normalization
    def add_normalization_not_equals(match):
        full_match = match.group(0)
        expected = match.group(1)
        # Skip if already has normalization
        if '.replace(/\\s/g, "")' in full_match:
            return full_match
        return f'if(a.replace(/\\s/g, "")!={expected}.replace(/\\s/g, ""))'
    
    # Find and update if(a==...) patterns
    pattern_equals = r'if\(a==([^)]+)\)'
    content = re.sub(pattern_equals, add_normalization_equals, content)
    
    # Find and update if(a!=...) patterns
    pattern_not_equals = r'if\(a!=([^)]+)\)'
    content = re.sub(pattern_not_equals, add_normalization_not_equals, content)
    
    if content != original_content:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
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
    # Check if file has output comparisons
    with open(filepath, 'r', encoding='utf-8') as f:
        file_content = f.read()
        if ('$("#output").text()' in file_content or 'getElementById("output")' in file_content) and ('if(a==' in file_content or 'if(a!=' in file_content):
            if fix_file(filepath):
                updated_count += 1
                print(f"Updated: {filepath}")

print(f"\nTotal files updated: {updated_count}")
