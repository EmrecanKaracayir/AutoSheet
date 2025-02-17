import os
from pathlib import Path

# Find current file path
current_path = Path(__file__).resolve().parent

# Define cache path
cache_path = current_path.parent / "data" / "cache"

# Create cache directory
os.makedirs(cache_path, exist_ok=True)
