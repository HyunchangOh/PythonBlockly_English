import os
import re
import glob

def update_file(filepath):
    """Update a single HTML file to add answer message functionality"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes_made = False
    
    # 1. Add answerMessage div if correctMessage exists and answerMessage doesn't
    if '<div id="correctMessage"' in content and '<div id="answerMessage"' not in content:
        content = re.sub(
            r'(<div id="correctMessage"[^>]*>.*?</div>)',
            r'\1\n<div id="answerMessage" class="correct-message"></div>',
            content,
            flags=re.DOTALL
        )
        changes_made = True
    
    # 2. Update showCorrectMessage timeout from 4000 to 3000
    if 'setTimeout(() => {\n      messageEl.style.display = \'none\';\n    }, 4000)' in content:
        content = content.replace(
            'setTimeout(() => {\n      messageEl.style.display = \'none\';\n    }, 4000)',
            'setTimeout(() => {\n      messageEl.style.display = \'none\';\n    }, 3000)'
        )
        changes_made = True
    elif 'setTimeout(() => {\n      messageEl.style.display = \'none\';\n    }, 4000);' in content:
        content = content.replace(
            'setTimeout(() => {\n      messageEl.style.display = \'none\';\n    }, 4000);',
            'setTimeout(() => {\n      messageEl.style.display = \'none\';\n    }, 3000);'
        )
        changes_made = True
    
    # 3. Add showAnswerMessage function if it doesn't exist
    if 'function showAnswerMessage' not in content and 'function showCorrectMessage' in content:
        # Find the showCorrectMessage function and add showAnswerMessage after it
        pattern = r'(function showCorrectMessage\(\) \{[^}]*\}[^}]*\}[^}]*\})'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            show_correct = match.group(0)
            show_answer = '''
  function showAnswerMessage(expectedAnswer) {
    const messageEl = document.getElementById('answerMessage');
    messageEl.textContent = "Expected answer: " + expectedAnswer;
    messageEl.style.display = 'block';
    messageEl.style.opacity = '1';
    setTimeout(() => {
      messageEl.style.opacity = '0';
    }, 2000);
    setTimeout(() => {
      messageEl.style.display = 'none';
    }, 3000);
  }'''
            content = content.replace(show_correct, show_correct + show_answer)
            changes_made = True
    
    # 4. Update submit button handlers - simple pattern: if(a=="expected")
    # Extract expected answer and add else clause
    pattern = r'(document\.getElementById\(\'submit\'\)\.addEventListener\(\'click\', function\(\) \{[^}]*?var a = \$\("#output"\)\.text\(\);\s*if\(a=="([^"]+)"\)\{[^}]*?showCorrectMessage\(\);\s*\}\s*\}\);)'
    def replace_simple_pattern(match):
        full_match = match.group(0)
        expected = match.group(1)
        # Check if else already exists
        if 'else{' in full_match or 'showAnswerMessage' in full_match:
            return full_match
        # Add expectedAnswer variable and else clause
        new_code = full_match.replace(
            f'if(a=="{expected}")',
            f'const expectedAnswer = "{expected}";\n    if(a==expectedAnswer)'
        ).replace(
            'showCorrectMessage();\n    }',
            'showCorrectMessage();\n    }\n    else{\n        showAnswerMessage(expectedAnswer);\n    }'
        )
        return new_code
    
    new_content = re.sub(pattern, replace_simple_pattern, content, flags=re.DOTALL)
    if new_content != content:
        content = new_content
        changes_made = True
    
    # 5. Update submit button handlers - check pattern: if(check) with choice variables
    # Find choice variables and add else clause
    pattern = r'(document\.getElementById\(\'submit\'\)\.addEventListener\(\'click\', function\(\) \{[^}]*?let check = true;[^}]*?(const choice\d+ = "[^"]+";[^}]*?)+[^}]*?if\(check\)\{[^}]*?showCorrectMessage\(\);\s*\}\s*\}\);)'
    def replace_check_pattern(match):
        full_match = match.group(0)
        if 'else{' in full_match or 'showAnswerMessage' in full_match:
            return full_match
        # Extract all choice variables
        choices = re.findall(r'const (choice\d+) = "([^"]+)";', full_match)
        if choices:
            # Create expected answer string
            if len(choices) == 1:
                expected = f'choice1'
                answer_text = choices[0][1]
            else:
                # Multiple choices - show all
                expected = '[' + ', '.join([f'{name}' for name, _ in choices]) + ']'
                answer_text = '\\n'.join([f'{name}: {val}' for name, val in choices])
            # Add else clause
            new_code = full_match.replace(
                'if(check){',
                f'if(check){'
            ).replace(
                'showCorrectMessage();\n    }',
                f'showCorrectMessage();\n    }}\n    else{{\n        const expectedAnswers = {expected};\n        showAnswerMessage(expectedAnswers);\n    }}'
            )
            return new_code
        return full_match
    
    new_content = re.sub(pattern, replace_check_pattern, content, flags=re.DOTALL)
    if new_content != content:
        content = new_content
        changes_made = True
    
    # Only write if changes were made
    if changes_made and content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Find all HTML files in docs directory
html_files = []
for root, dirs, files in os.walk('docs'):
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

updated_count = 0
for filepath in html_files:
    # Check if file has submit button
    with open(filepath, 'r', encoding='utf-8') as f:
        if "getElementById('submit')" in f.read():
            if update_file(filepath):
                updated_count += 1
                print(f"Updated: {filepath}")

print(f"\nTotal files updated: {updated_count}")
