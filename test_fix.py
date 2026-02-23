with open('docs/new1/Code_1_Aufgabe_1.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("BEFORE:")
idx = content.find('if(a')
print(content[idx:idx+150])

# Replace
content = content.replace('.replace(/\\n/g, " ").replace(/\\s+/g, " ").trim()', '.replace(/\\s/g, "")')

print("\nAFTER:")
idx = content.find('if(a')
print(content[idx:idx+150])

with open('docs/new1/Code_1_Aufgabe_1.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nFile updated!")
