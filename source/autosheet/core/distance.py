import cv2
import numpy as np

from autosheet.core import glyph
from autosheet.data import distances
from autosheet.data.models.Distance import Distance
from autosheet.utils import chars, constants, paths


def get_distance(g1: str, g2: str) -> float:
    """
    Get the distance between two grayscale images.
    """
    cache = distances.get_distances()

    # Ensure the subject is always the lexicographically smaller glyph
    subject = min(g1, g2)
    target = max(g1, g2)

    # If the subject is not in the cache, add it
    if subject not in cache:
        cache[subject] = []

    # Lookup the distance in the cache
    for distance in cache[subject]:
        if distance.target == target:
            return distance.distance

    # Get the masks for the two glyphs
    m1 = glyph.get_glyph_mask(g1)
    m2 = glyph.get_glyph_mask(g2)

    # Compute the distance between the two images and save it to the cache
    distance = _compute_distance(g1, m1, g2, m2)

    # Add the target distance to the cache
    cache[subject].append(Distance(target, distance))

    # Save the updated cache
    distances.save_distances()

    # Return the computed distance
    return distance


def _compute_distance(g1: str, m1: np.ndarray, g2: str, m2: np.ndarray) -> float:
    """
    Computes a per-pixel absolute distance between two grayscale images.
    """
    distance = np.abs(m1 - m2)
    total_distance = distance.sum()

    # Save the difference image to the debug folder
    if constants.DEBUG:
        glyph1_name = chars.get_safe_name(g1)
        glyph2_name = chars.get_safe_name(g2)
        cv2.imwrite(
            str(
                paths.get_path(
                    paths.DEBUG_DISTANCED_FOLDER
                    / f"{glyph1_name}---{glyph2_name}.{constants.IMAGE_FORMAT}"
                )
            ),
            distance,
        )

    # Return the average difference
    return total_distance
