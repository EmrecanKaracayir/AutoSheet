import os
import sys
from pathlib import Path

from autosheet.utils import constants

RESOURCES_FOLDER: Path = Path("resources")
FONT_FILE: Path = RESOURCES_FOLDER / constants.FONT_NAME

DATA_FOLDER: Path = Path("data")
IMAGES_FOLDER: Path = DATA_FOLDER / "images"
PDFS_FOLDER: Path = DATA_FOLDER / "pdfs"

CACHE_FOLDER: Path = DATA_FOLDER / "cache"
GLYPHS_FOLDER: Path = CACHE_FOLDER / "glyphs"
DISTANCES_FILE: Path = CACHE_FOLDER / "distances.json"
MATCHES_FILE: Path = CACHE_FOLDER / "matches.json"

DEBUG_FOLDER: Path = CACHE_FOLDER / "debug"
DEBUG_DISTANCED_FOLDER: Path = DEBUG_FOLDER / "distanced"
DEBUG_PROCESSED_FOLDER: Path = DEBUG_FOLDER / "processed"


def get_path(relative_path: Path) -> Path:
    """
    Get the absolute path to the resource.
    """
    try:
        # When bundled, PyInstaller places resources in the _MEIPASS folder.
        base_path = sys._MEIPASS
    except Exception:
        # When running in a normal Python process, use the directory of the script.
        base_path = os.path.abspath(".")

    return Path(base_path) / relative_path
