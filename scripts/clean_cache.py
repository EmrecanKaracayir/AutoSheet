from pathlib import Path

# Remove all files and folders in the data/cache folder
[p.unlink() for p in Path("data/cache").rglob("*") if p.is_file() or p.is_symlink()]
