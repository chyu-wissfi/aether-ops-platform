import os
from pathlib import Path

def tree(dir_path, prefix='', level=-1):
    if level == 0:
        return
    dir_path = Path(dir_path)
    entries = sorted(dir_path.iterdir(), key=lambda e: (e.is_file(), e.name))
    pointers = ['├── '] * (len(entries) - 1) + ['└── ']
    for pointer, path in zip(pointers, entries):
        print(f'{prefix}{pointer}{path.name}{"/" if path.is_dir() else ""}')
        if path.is_dir():
            extension = '│   ' if pointer == '├── ' else '    '
            tree(path, prefix + extension, level - 1)

if __name__ == '__main__':
    api_dir = '/home/wissfi/projects/LLMOps/api'
    print(f'{os.path.basename(api_dir)}/')
    tree(api_dir, level=4)
