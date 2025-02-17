import os
from pathlib import Path

# Find current file path
current_path = Path(__file__).resolve().parent

# Define cache path
cache_path = current_path.parent / "data" / "cache"

# Create cache directory
os.makedirs(cache_path, exist_ok=True)

# Define glyphs path
glyphs_path = cache_path / "glyphs"

# Create glyphs directory
os.makedirs(glyphs_path, exist_ok=True)

# Define debug path
debug_path = cache_path / "debug"

# Create debug directory
os.makedirs(debug_path, exist_ok=True)

# Define distanced path
distanced_path = debug_path / "distanced"

# Create distanced directory
os.makedirs(distanced_path, exist_ok=True)

# Define processed path
processed_path = debug_path / "processed"

# Create processed directory
os.makedirs(processed_path, exist_ok=True)
