import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from PIL.ImageFont import FreeTypeFont

from autosheet.data import font
from autosheet.utils import chars, constants, paths


def get_glyph_mask(glyph: str) -> np.ndarray:
    """
    Get the blurred mask for a given glyph. The mask is cached for future use.
    """
    path = paths.get_path(
        paths.GLYPHS_FOLDER / f"{chars.get_safe_name(glyph)}.{constants.IMAGE_FORMAT}"
    )

    # Load the cached glyph if it exists
    if path.exists():
        return cv2.imread(str(path), cv2.IMREAD_GRAYSCALE).astype("float")

    # Render the glyph and save it to the cache
    mask = _render_glyph_mask(glyph)
    cv2.imwrite(str(path), mask)
    return mask


def _render_glyph_mask(
    glyph: str,
    size: int = constants.CANVAS_SIZE,
    font: FreeTypeFont = font.get_font(),
    blur_radius: int = constants.BLUR_RADIUS,
) -> np.ndarray:
    """
    Render a character as a blurred mask.
    """
    # Create a new grayscale image with a black background
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)

    # Calculate centered position for the glyph
    left, _, right, _ = draw.textbbox((0, 0), glyph, font=font)
    w = right - left
    ascent, descent = font.getmetrics()
    baseline = (size + (ascent - descent)) / 2
    x = (size - w) / 2 - left
    y = baseline - ascent

    # Draw the glyph in white (full intensity)
    draw.text((x, y), glyph, fill=255, font=font)

    # Apply a Gaussian blur to get the optical footprint
    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))
    return np.array(mask, dtype="float")
