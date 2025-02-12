import json

from autosheet.data.models.Distance import Distance
from autosheet.utils import paths

_DISTANCES: dict[str, list[Distance]] | None = None


def get_distances() -> dict:
    """
    Load the precomputed distances from the cache.
    """
    global _DISTANCES

    # Return the cached distances if they are already loaded
    if _DISTANCES is not None:
        return _DISTANCES

    # Load the distances from the cache file
    try:
        with open(paths.DISTANCES_FILE) as f:
            data = json.load(f)
        _DISTANCES = {}

        # Map the loaded data to Distance objects
        for subject, distances in data.items():
            _DISTANCES[subject] = [Distance.from_dict(d) for d in distances]
    except Exception:
        _DISTANCES = {}

    # Return the loaded distances
    return _DISTANCES


def save_distances() -> None:
    """
    Save the precomputed distances to the cache.
    """
    global _DISTANCES

    # Serialize the distances to a dictionary
    data = {subject: [d.to_dict() for d in distances] for subject, distances in _DISTANCES.items()}

    # Save the distances to the cache file
    with open(paths.DISTANCES_FILE, "w") as f:
        json.dump(data, f, indent=2)
