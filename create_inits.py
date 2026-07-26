"""Create all __init__.py files for WEBSTER project."""
import os

base = r"c:\Users\Kshitij Kadulkar\Documents\AURA\webster"

folders = [
    'config', 'core', 'ai', 'memory', 'voice', 'ui', 'study',
    'automation', 'dashboard', 'mobile', 'widgets', 'plugins',
    'floater', 'sync'
]

subfolders = [
    'components', 'pages', 'containers', 'widgets',
    'dashboard', 'orb', 'status', 'animations'
]

for f in folders:
    path = os.path.join(base, f, '__init__.py')
    with open(path, 'w') as fp:
        fp.write('')

for f in subfolders:
    path = os.path.join(base, 'ui', f, '__init__.py')
    with open(path, 'w') as fp:
        fp.write('')

print("All __init__.py files created successfully!")
print(f"Total: {len(folders) + len(subfolders)} files")
