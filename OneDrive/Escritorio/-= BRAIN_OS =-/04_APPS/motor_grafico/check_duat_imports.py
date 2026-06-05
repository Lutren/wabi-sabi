import os, sys

def find_imports(root, module_name):
    """Search for imports of module_name (without .py) in .py files under root."""
    matches = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip excluded dirs
        if any(ex in dirpath for ex in ['.git', '__pycache__', '_archive', '_snapshots', '_reports']):
            continue
        for f in filenames:
            if f.endswith('.py'):
                fp = os.path.join(dirpath, f)
                try:
                    with open(fp, 'r', encoding='utf-8', errors='ignore') as ff:
                        content = ff.read()
                        if module_name in content:
                            matches.append(fp)
                except Exception:
                    pass
    return matches

root = r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-"
modules = [
    'duat_core_fast',
    'duat_core_minimal',
    'duat_core_optimized',
    'duat_core_osit_v3',
    'duat_core_v0.2',
    'duat_core_v0.3'
]

for mod in modules:
    matches = find_imports(root, mod)
    print(f"{mod}: {len(matches)} matches")
    if matches:
        for m in matches[:5]:  # show first 5
            print("  ", m)
    print()