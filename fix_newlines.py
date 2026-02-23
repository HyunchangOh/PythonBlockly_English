import re

files_to_fix = [
    'docs/new1/Code_1_Aufgabe_1.html',
    'docs/new1/1_aufgabe1.html'
]

for filepath in files_to_fix:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace old normalization with new one
    old_pattern = r'\.replace\(/\\n/g, ""\)'
    # Use a function to properly escape the replacement
    def replace_func(match):
        return '.replace(/\\n/g, " ").replace(/\\s+/g, " ").trim()'
    
    new_content = re.sub(old_pattern, replace_func, content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {filepath}")
    else:
        print(f"No changes needed: {filepath}")
