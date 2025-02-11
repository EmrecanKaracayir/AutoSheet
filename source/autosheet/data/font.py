from PIL import ImageFont

from autosheet.utils import constants, paths

_FONT = None


def get_font():
    """
    Get the font for rendering glyphs.
    """
    global _FONT

    # Return the cached font if it exists
    if _FONT is not None:
        return _FONT

    # Load the font from the file system
    _FONT = ImageFont.truetype(str(paths.FONT_PATH), constants.FONT_SIZE)
    return _FONT
