import os

html_files = []
for root, dirs, files in os.walk('docs'):
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

updated = 0
for filepath in html_files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Replace old patterns
        content = content.replace('.replace(/\\n/g, " ").replace(/\\s+/g, " ").trim()', '.replace(/\\s/g, "")')
        content = content.replace('.replace(/\\n/g, "")', '.replace(/\\s/g, "")')
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            updated += 1
            print(f"Updated: {filepath}")
    except:
        pass

print(f"\nTotal files updated: {updated}")
