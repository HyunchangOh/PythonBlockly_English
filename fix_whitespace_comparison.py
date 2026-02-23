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
    changes_made = False
    
    # Replace any existing normalization with simple whitespace removal
    # Pattern 1: Old normalization .replace(/\n/g, "")
    old_pattern1 = r'\.replace\(/\\n/g, ""\)'
    # Pattern 2: New normalization with spaces
    old_pattern2 = r'\.replace\(/\\n/g, " "\)\.replace\(/\\s\+/g, " "\)\.trim\(\)'
    
    def replace_with_simple(match):
        return '.replace(/\\s/g, "")'
    
    # Replace old patterns - need to escape properly
    # First replace the complex pattern
    new_content = re.sub(r'\.replace\(/\\n/g, " "\)\.replace\(/\\s\+/g, " "\)\.trim\(\)', '.replace(/\\s/g, "")', content)
    # Then replace the simple pattern
    new_content = re.sub(r'\.replace\(/\\n/g, ""\)', '.replace(/\\s/g, "")', new_content)
    
    # Also handle patterns that might not have normalization yet
    # Pattern: if(a==expectedAnswer) or if(a!=choice1)
    def add_normalization_equals(match):
        full_match = match.group(0)
        expected = match.group(1)
        # Skip if already has normalization
        if '.replace(/\\s/g, "")' in full_match:
            return full_match
        return f'if(a.replace(/\\s/g, "")=={expected}.replace(/\\s/g, ""))'
    
    def add_normalization_not_equals(match):
        full_match = match.group(0)
        expected = match.group(1)
        # Skip if already has normalization
        if '.replace(/\\s/g, "")' in full_match:
            return full_match
        return f'if(a.replace(/\\s/g, "")!={expected}.replace(/\\s/g, ""))'
    
    # Find and update if(a==...) patterns
    pattern_equals = r'if\(a==([^)]+)\)'
    new_content = re.sub(pattern_equals, add_normalization_equals, new_content)
    
    # Find and update if(a!=...) patterns
    pattern_not_equals = r'if\(a!=([^)]+)\)'
    new_content = re.sub(pattern_not_equals, add_normalization_not_equals, new_content)
    
    if new_content != original_content:
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
    # Check if file has output comparisons
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        if ('$("#output").text()' in content or 'getElementById("output")' in content) and ('if(a==' in content or 'if(a!=' in content):
            if fix_file(filepath):
                updated_count += 1
                print(f"Updated: {filepath}")

print(f"\nTotal files updated: {updated_count}")
