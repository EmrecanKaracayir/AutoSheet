from autosheet.core import glyph
from autosheet.utils import chars, constants, paths


def test_get_glyph_mask():
    test_glyph = "A"
    mask = glyph.get_glyph_mask(test_glyph)

    # Check the mask properties
    assert mask is not None
    assert mask.shape == (constants.CANVAS_SIZE, constants.CANVAS_SIZE)
    assert mask.dtype == "float"

    # Check if glyph is cached
    assert (
        paths.GLYPHS_PATH / f"{chars.get_safe_name(test_glyph)}.{constants.IMAGE_FORMAT}"
    ).exists()
