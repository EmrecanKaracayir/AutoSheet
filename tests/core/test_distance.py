from autosheet.core import distance
from autosheet.utils import constants


def test_get_distance() -> None:
    # Set debug mode to True
    constants.DEBUG = True

    # Start testing
    test_g1 = "A"

    # Compute the distance between the mask and itself
    assert distance.get_distance(test_g1, test_g1) == 0

    # Compute the difference between two largely different masks
    test_g1 = "A"
    test_g2 = "B"

    large_distance = distance.get_distance(test_g1, test_g2)

    # Reverse the order of the masks
    reverse_distance = distance.get_distance(test_g2, test_g1)

    assert large_distance == reverse_distance

    # Compute the difference between two similar masks
    test_g1 = "B"
    test_g2 = "8"

    small_distance = distance.get_distance(test_g1, test_g2)

    assert large_distance > small_distance

    # Compute all glyph differences
    glyphs = list("0123456789") + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    glyphs.append("")
    for i, g1 in enumerate(glyphs):
        for j, g2 in enumerate(glyphs):
            if j < i:
                continue
            distance.get_distance(g1, g2)
