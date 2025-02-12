from pathlib import Path

from autosheet.utils import constants

RESOURCES_FOLDER: Path = Path("resources")
FONT_FILE: Path = RESOURCES_FOLDER / constants.FONT_NAME

DATA_FOLDER: Path = Path("data")
IMAGES_FOLDER: Path = DATA_FOLDER / "images"
PDFS_FOLDER: Path = DATA_FOLDER / "pdfs"

CACHE_FOLDER: Path = DATA_FOLDER / "cache"
DEBUG_FOLDER: Path = CACHE_FOLDER / "debug"
GLYPHS_FOLDER: Path = CACHE_FOLDER / "glyphs"
DISTANCES_FILE: Path = CACHE_FOLDER / "distances.json"
MATCHES_FILE: Path = CACHE_FOLDER / "matches.json"
