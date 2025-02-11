import json

from autosheet.utils import paths

_DISTANCES = None


def get_distances():
    """
    Load the precomputed distances from the cache.
    """
    global _DISTANCES

    # Return the cached distances if they are already loaded
    if _DISTANCES is not None:
        return _DISTANCES

    # Load the distances from the cache file
    try:
        with open(paths.DISTANCES_PATH) as f:
            _DISTANCES = json.load(f)
    except:
        _DISTANCES = {}

    # Return the loaded distances
    return _DISTANCES


def save_distances():
    """
    Save the precomputed distances to the cache.
    """
    global _DISTANCES

    # Save the distances to the cache file
    with open(paths.DISTANCES_PATH, "w") as f:
        json.dump(_DISTANCES, f, indent=2)
