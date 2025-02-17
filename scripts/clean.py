import shutil
from pathlib import Path

# Remove .pytest_cache folder
[shutil.rmtree(p) for p in Path(".").rglob(".pytest_cache") if p.is_dir()]

# Remove package folder
[shutil.rmtree(p) for p in [Path("package")] if p.exists()]

# Remove all __pycache__ folders
[shutil.rmtree(p) for p in list(Path(".").rglob("__pycache__")) if p.is_dir()]

# Remove all *.pyc files
[p.unlink() for p in list(Path(".").rglob("*.pyc")) if p.is_file()]

# Remove all *.egg-info folders
[shutil.rmtree(p) for p in list(Path(".").rglob("*.egg-info")) if p.is_dir()]
