import os
import re
import glob

def normalize_newlines_in_comparisons(content):
    """Update comparison logic to normalize newlines (accept both with and without newlines)"""
    original_content = content
    changes_made = False
    
    # Skip if already normalized
    if '.replace(/\\n/g, "")' in content:
        return content, False
    
    # Pattern 1: if(a==expectedAnswer) or if(a=="...")
    # Match: if(a==expectedAnswer) or if(a=="string")
    def replace_equals(match):
        full_match = match.group(0)
        # Check if already normalized
        if '.replace(/\\n/g, "")' in full_match:
            return full_match
        
        # Extract the expected value
        expected = match.group(1)
        
        # Replace with normalized version
        if expected.startswith('"') and expected.endswith('"'):
            # String literal - need to handle escaped quotes
            return f'if(a.replace(/\\n/g, "")=={expected}.replace(/\\n/g, ""))'
        else:
            # Variable
            return f'if(a.replace(/\\n/g, "")=={expected}.replace(/\\n/g, ""))'
    
    pattern1 = r'if\(a==([^)]+)\)'
    new_content = re.sub(pattern1, replace_equals, content)
    if new_content != content:
        content = new_content
        changes_made = True
    
    # Pattern 2: if(a!=choice1) or if(a!="...")
    def replace_not_equals(match):
        full_match = match.group(0)
        # Check if already normalized
        if '.replace(/\\n/g, "")' in full_match:
            return full_match
        
        # Extract the expected value
        expected = match.group(1)
        
        # Replace with normalized version
        if expected.startswith('"') and expected.endswith('"'):
            # String literal
            return f'if(a.replace(/\\n/g, "")!={expected}.replace(/\\n/g, ""))'
        else:
            # Variable
            return f'if(a.replace(/\\n/g, "")!={expected}.replace(/\\n/g, ""))'
    
    pattern2 = r'if\(a!=([^)]+)\)'
    new_content = re.sub(pattern2, replace_not_equals, content)
    if new_content != content:
        content = new_content
        changes_made = True
    
    return content, changes_made

def update_file(filepath):
    """Update a single HTML file to normalize newlines in comparisons"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False
    
    original_content = content
    content, changes_made = normalize_newlines_in_comparisons(content)
    
    # Only write if changes were made
    if changes_made and content != original_content:
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
        content = f.read()
        if ('$("#output").text()' in content or 'getElementById("output")' in content) and ('if(a==' in content or 'if(a!=' in content):
            if update_file(filepath):
                updated_count += 1
                print(f"Updated: {filepath}")

print(f"\nTotal files updated: {updated_count}")
