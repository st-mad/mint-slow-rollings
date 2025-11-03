"""Quick import checker for the project's main dependencies.

Run this inside the created venv to verify that Python packages and system deps (like graphviz) are available.
"""
import importlib
deps = [
    'ply',
    'matplotlib',
    'networkx',
    'pygraphviz',
    'pydot',
    'tkinter',
]

failed = []
for d in deps:
    try:
        importlib.import_module(d)
        print(f"OK: {d}")
    except Exception as e:
        print(f"FAIL: {d} -> {e}")
        failed.append((d, str(e)))

if failed:
    print('\nSome imports failed. Common causes:')
    print('- pygraphviz/pydot may require system Graphviz installed (brew install graphviz on macOS).')
    print('- tkinter may not be available in some Python builds; use the macOS system Python or install python via Homebrew with tkinter support.')
    raise SystemExit(1)
else:
    print('\nAll imports OK')
