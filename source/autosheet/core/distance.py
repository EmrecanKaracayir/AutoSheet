import cv2
import numpy as np

from autosheet.data import distances
from autosheet.utils import chars, constants, paths


def get_distance(glyph1, mask1, glyph2, mask2):
    """
    Get the distance between two grayscale images.
    """
    DISTANCES = distances.get_distances()

    # Get the key for the distance cache
    key = f"{min(glyph1, glyph2)}_{max(glyph1, glyph2)}"
    if key in DISTANCES:
        return DISTANCES[key]

    # Compute the distance between the two images and save it to the cache
    distance = _compute_distance(glyph1, mask1, glyph2, mask2)
    DISTANCES[key] = float(distance)
    distances.save_distances()

    # Return the computed distance
    return distance


def _compute_distance(glyph1, mask1, glyph2, mask2):
    """
    Computes a per-pixel absolute distance between two grayscale images.
    Returns the total distance.
    """
    distance = np.abs(mask1 - mask2)
    total_distance = distance.sum()

    # Get safe names for the glyphs
    glyph1_name = chars.get_safe_name(glyph1)
    glyph2_name = chars.get_safe_name(glyph2)

    # Save the difference image to the debug folder
    if constants.DEBUG:
        cv2.imwrite(
            str(paths.DEBUG_PATH / f"{glyph1_name}-{glyph2_name}.{constants.IMAGE_FORMAT}"),
            distance,
        )

    # Return the average difference
    return total_distance
