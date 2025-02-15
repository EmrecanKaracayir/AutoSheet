import json

from autosheet.data.models.Match import Match
from autosheet.utils import paths

_MATCHES: dict[str, list[Match]] | None = None


def get_matches() -> dict:
    """
    Load the precomputed mathes from the cache.
    """
    global _MATCHES

    # Return the cached matches if they are already loaded
    if _MATCHES is not None:
        return _MATCHES

    # Load the matches from the cache file
    try:
        with open(paths.get_path(paths.MATCHES_FILE)) as f:
            data = json.load(f)
        _MATCHES = {}

        # Map the loaded data to Match objects
        for subject, distances in data.items():
            _MATCHES[subject] = [Match.from_dict(d) for d in distances]
    except Exception:
        _MATCHES = {}

    # Return the loaded distances
    return _MATCHES


def save_matches() -> None:
    """
    Save the precomputed mathes to the cache.
    """
    global _MATCHES

    # Serialize the matches to a dictionary
    data = {subject: [d.to_dict() for d in distances] for subject, distances in _MATCHES.items()}

    # Save the matches to the cache file
    with open(paths.get_path(paths.MATCHES_FILE), "w") as f:
        json.dump(data, f, indent=2)
