import os
os.makedirs('terminal_buddy', exist_ok=True)

def w(path, lines):
    with open(path, 'w') as f:
        f.write(chr(10).join(lines))
    print("Created " + path)
