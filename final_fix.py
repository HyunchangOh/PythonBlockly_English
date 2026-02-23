import os
import re

def fix_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False
    
    original = content
    
    # Replace all normalization patterns with simple whitespace removal
    content = content.replace('.replace(/\\n/g, " ").replace(/\\s+/g, " ").trim()', '.replace(/\\s/g, "")')
    content = content.replace('.replace(/\\n/g, "")', '.replace(/\\s/g, "")')
    
    # Also handle unnormalized comparisons
    def fix_equals(m):
        s = m.group(0)
        if '.replace(/\\s/g, "")' in s:
            return s
        expected = m.group(1)
        return f'if(a.replace(/\\s/g, "")=={expected}.replace(/\\s/g, ""))'
    
    def fix_not_equals(m):
        s = m.group(0)
        if '.replace(/\\s/g, "")' in s:
            return s
        expected = m.group(1)
        return f'if(a.replace(/\\s/g, "")!={expected}.replace(/\\s/g, ""))'
    
    content = re.sub(r'if\(a==([^)]+)\)', fix_equals, content)
    content = re.sub(r'if\(a!=([^)]+)\)', fix_not_equals, content)
    
    if content != original:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except:
            return False
    return False

html_files = []
for root, dirs, files in os.walk('docs'):
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

updated = 0
for filepath in html_files:
    # Read once to check
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            c = f.read()
        if ('$("#output").text()' in c or 'getElementById("output")' in c) and ('if(a==' in c or 'if(a!=' in c):
            # Now fix it
            if fix_file(filepath):
                updated += 1
                print(f"Updated: {filepath}")
    except:
        pass

print(f"\nTotal files updated: {updated}")
